-- Workflows Table
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    workflow_id UUID UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    dataset_path VARCHAR(255),
    model_path VARCHAR(255),
    protected_attributes TEXT[] NOT NULL,
    target_column VARCHAR(100) NOT NULL,
    metadata JSONB,
    INDEX idx_workflow_status (status),
    INDEX idx_workflow_created (created_at)
);

-- Workflow Steps Table
CREATE TABLE workflow_steps (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    agent_name VARCHAR(100) NOT NULL,
    step_sequence INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    UNIQUE(workflow_id, step_sequence),
    INDEX idx_workflow_steps (workflow_id, status)
);

-- Metrics Results Table
CREATE TABLE metrics_results (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    agent_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    threshold_value FLOAT,
    passed_threshold BOOLEAN,
    affected_groups TEXT[] NOT NULL,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    INDEX idx_metrics_workflow (workflow_id),
    INDEX idx_metrics_agent (agent_name)
);

-- Root Cause Analysis Table
CREATE TABLE root_cause_analysis (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    feature_name VARCHAR(100) NOT NULL,
    importance_score FLOAT,
    correlation_with_target FLOAT,
    correlation_with_protected_attr FLOAT,
    is_proxy BOOLEAN DEFAULT false,
    evidence TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rca_workflow (workflow_id)
);

-- Mitigation Strategies Table
CREATE TABLE mitigation_strategies (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    strategy_type VARCHAR(50) NOT NULL,
    strategy_name VARCHAR(100) NOT NULL,
    description TEXT,
    parameters JSONB,
    expected_fairness_improvement FLOAT,
    expected_accuracy_impact FLOAT,
    complexity_score FLOAT,
    recommended BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_mitigation_workflow (workflow_id)
);

-- Validation Results Table
CREATE TABLE validation_results (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    strategy_id INTEGER NOT NULL REFERENCES mitigation_strategies(id),
    fairness_metrics JSONB,
    accuracy_metrics JSONB,
    improvement_percentage FLOAT,
    validation_status VARCHAR(50),
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_validation_workflow (workflow_id)
);

-- Monitoring Data Table
CREATE TABLE monitoring_data (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER,
    metric_type VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_anomaly BOOLEAN DEFAULT false,
    alert_sent BOOLEAN DEFAULT false,
    INDEX idx_monitoring_time (recorded_at),
    INDEX idx_monitoring_metric (metric_type)
);

-- Agent Logs Table
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflows(id),
    agent_name VARCHAR(100) NOT NULL,
    log_level VARCHAR(20),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_logs_workflow (workflow_id),
    INDEX idx_logs_timestamp (timestamp)
);
