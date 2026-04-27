import pandas as pd
import numpy as np
from aif360.datasets import StandardDataset
import pickle
import logging

logger = logging.getLogger(__name__)

class MetricsCalculator:
    def __init__(self):
        self.protected_attribute_names = None
        self.target_attribute_name = None

    def load_dataset(self, dataset_path: str) -> pd.DataFrame:
        """Load dataset from CSV or parquet"""
        if dataset_path.endswith('.csv'):
            return pd.read_csv(dataset_path)
        elif dataset_path.endswith('.parquet'):
            return pd.read_parquet(dataset_path)
        else:
            raise ValueError(f"Unsupported format: {dataset_path}")

    def load_model(self, model_path: str):
        """Load trained model from pickle"""
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    def prepare_aif360_dataset(self, df: pd.DataFrame, protected_attributes: list,
                              target_name: str, privileged_groups: dict = None):
        """Convert pandas DataFrame to AIF360 StandardDataset"""
        feature_names = [col for col in df.columns
                        if col != target_name and col not in protected_attributes]

        dataset = StandardDataset(
            df=df,
            label_name=target_name,
            favorable_classes=[1, 'positive', 'approved'],
            protected_attribute_names=protected_attributes,
            privileged_classes=privileged_groups,
            features_to_keep=feature_names
        )

        return dataset

    def compute_disparate_impact_ratio(self, y_pred: np.ndarray, protected_attr: np.ndarray,
                                       privileged_group_value) -> float:
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask

        p_favorable_privileged = y_pred[privileged_mask].mean()
        p_favorable_unprivileged = y_pred[unprivileged_mask].mean()

        if p_favorable_privileged == 0:
            return 0.0

        di_ratio = p_favorable_unprivileged / p_favorable_privileged
        return float(di_ratio)

    def compute_equal_opportunity_difference(self, y_true: np.ndarray, y_pred: np.ndarray,
                                            protected_attr: np.ndarray,
                                            privileged_group_value) -> float:
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask

        tpr_privileged = (y_pred[privileged_mask] == y_true[privileged_mask]).mean()
        tpr_unprivileged = (y_pred[unprivileged_mask] == y_true[unprivileged_mask]).mean()

        return float(tpr_unprivileged - tpr_privileged)

    def compute_demographic_parity(self, y_pred: np.ndarray, protected_attr: np.ndarray,
                                   privileged_group_value) -> tuple:
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask

        p_favorable_privileged = y_pred[privileged_mask].mean()
        p_favorable_unprivileged = y_pred[unprivileged_mask].mean()

        difference = abs(p_favorable_privileged - p_favorable_unprivileged)
        threshold = 0.10

        is_satisfied = difference <= threshold
        return (is_satisfied, float(difference))

    def compute_calibration(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                           protected_attr: np.ndarray, privileged_group_value) -> float:
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask

        calib_priv = np.abs(y_pred_proba[privileged_mask] - y_true[privileged_mask]).mean()
        calib_unpriv = np.abs(y_pred_proba[unprivileged_mask] - y_true[unprivileged_mask]).mean()

        return float(abs(calib_priv - calib_unpriv))

    def compute_all_metrics(self, dataset, model, protected_attributes: list,
                           target_column: str, privileged_groups: dict = None) -> dict:
        results = {
            'disparate_impact_ratio': {},
            'equal_opportunity_difference': {},
            'demographic_parity': {},
            'calibration_difference': {},
            'affected_groups': [],
            'overall_fairness_status': 'FAIR'
        }

        try:
            X = dataset.drop(columns=[target_column] + protected_attributes)
            y_true = dataset[target_column].values
            y_pred = model.predict(X).astype(int)

            for attr in protected_attributes:
                protected_values = dataset[attr].unique()
                attr_results = {}

                for privilege_value in protected_values:
                    di_ratio = self.compute_disparate_impact_ratio(
                        y_pred, dataset[attr].values, privilege_value
                    )
                    attr_results[f'{privilege_value}_di_ratio'] = di_ratio

                    if di_ratio < 0.80:
                        results['affected_groups'].append(attr)
                        results['overall_fairness_status'] = 'BIASED'

                    eod = self.compute_equal_opportunity_difference(
                        y_true, y_pred, dataset[attr].values, privilege_value
                    )
                    attr_results[f'{privilege_value}_eod'] = eod

                    dp_satisfied, dp_diff = self.compute_demographic_parity(
                        y_pred, dataset[attr].values, privilege_value
                    )
                    attr_results[f'{privilege_value}_dp_satisfied'] = dp_satisfied
                    attr_results[f'{privilege_value}_dp_difference'] = dp_diff

                results[f'{attr}_metrics'] = attr_results

            logger.info(f"Computed metrics: {results['overall_fairness_status']}")

        except Exception as e:
            logger.error(f"Error computing metrics: {str(e)}")
            results['error'] = str(e)

        return results
