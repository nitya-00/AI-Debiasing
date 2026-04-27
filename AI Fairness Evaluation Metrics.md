# AGENTIC AI FAIRNESS SYSTEM - DETAILED TECH STACK & IMPLEMENTATION GUIDE

---

## TABLE OF CONTENTS
1. [Detailed Tech Stack Table](#detailed-tech-stack-table)
2. [Project Structure](#project-structure)
3. [Component-wise Implementation](#component-wise-implementation)
4. [Setup Instructions](#setup-instructions)
5. [API Contracts](#api-contracts)
6. [Database Schema](#database-schema)
7. [Configuration Files](#configuration-files)

--- 

# DETAILED TECH STACK TABLE

## 1. API GATEWAY & ORCHESTRATION LAYER
### **AMAN'S PRIMARY RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Framework** | Spring Boot | 3.2.x | REST API endpoint & request handling | `spring-boot-starter-web` | See [Spring Setup](#spring-boot-setup) |
| **Build Tool** | Maven | 3.8.x | Dependency management & build | `mvn install` | [pom.xml](#pomxml) |
| **Java Version** | OpenJDK | 17 LTS | Runtime environment | `apt install openjdk-17-jdk` | N/A |
| **Embedded Server** | Tomcat | 10.1.x (built-in) | HTTP server | Auto-configured by Spring Boot | N/A |
| **Dependency Injection** | Spring DI | Built-in | Object lifecycle management | `@Autowired`, `@Service` | [Example](#spring-di-example) |
| **REST Framework** | Spring MVC | Built-in | Controller mapping | `@RestController`, `@PostMapping` | [Controller Example](#controller-example) |
| **Validation** | Jakarta Validation | 3.0.x | Input validation | `@Valid`, `@NotNull` annotations | [Validation Example](#validation-example) |
| **JSON Processing** | Jackson | 2.15.x | JSON serialization | `ObjectMapper` | [JSON Example](#json-example) |
| **Async Processing** | Spring Async | Built-in | Non-blocking requests | `@Async`, `@EnableAsync` | [Async Example](#async-example) |

---

## 2. MESSAGE QUEUE & EVENT STREAMING
### **AMAN'S RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Message Broker** | Apache Kafka | 3.6.x | Agent-to-agent communication | `docker run confluentinc/cp-kafka:7.6.0` | [Kafka Config](#kafka-config) |
| **Kafka Topics** | 5 Topics | - | Different agent queues | Create via `kafka-topics.sh` or admin API | [Topic Setup](#kafka-topics) |
| **Producer** | Spring Kafka | 3.1.x | Publish messages | `spring-kafka` dependency | [Producer Example](#kafka-producer) |
| **Consumer** | Spring Kafka Listener | 3.1.x | Subscribe to messages | `@KafkaListener` annotation | [Consumer Example](#kafka-consumer) |
| **Serialization** | JSON (Jackson) | 2.15.x | Message format | Spring Kafka auto-config | [Serialization Example](#kafka-serialization) |
| **Acknowledgment** | Auto-commit | Configurable | Message processing guarantee | `spring.kafka.consumer.auto-offset-reset` | [ACK Config](#kafka-ack) |
| **Error Handling** | Dead Letter Topic (DLT) | Built-in | Failed message handling | `@DltHandler` annotation | [DLT Example](#kafka-dlt) |

**Kafka Topics to Create:**
```
1. agent-bias-detection-requests
2. agent-root-cause-requests
3. agent-mitigation-requests
4. agent-validation-requests
5. agent-monitoring-requests
6. agent-results (for all results)
```

---

## 3. DATABASE & PERSISTENCE LAYER
### **AMAN'S RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Database** | PostgreSQL | 15.x | Persistent storage | `docker run postgres:15-alpine` | [DB Setup](#postgres-setup) |
| **JDBC Driver** | PostgreSQL JDBC | 42.7.x | Java-Database connection | `org.postgresql:postgresql:42.7.x` | Auto-configured |
| **ORM Framework** | Spring Data JPA | 3.2.x | Object-Relational Mapping | `spring-boot-starter-data-jpa` | [JPA Example](#jpa-example) |
| **Database Access** | Hibernate | 6.2.x | JPA implementation | Included in Spring Data JPA | [Hibernate Config](#hibernate-config) |
| **Connection Pooling** | HikariCP | 5.1.x | Connection management | `spring.datasource.hikari.*` | [HikariCP Config](#hikaricp-config) |
| **Migration Tool** | Flyway | 9.22.x | Database version control | `spring-boot-starter-flyway` | [Migration Example](#flyway-example) |
| **Query Language** | JPQL/SQL | - | Data querying | Native queries in @Query | [Query Example](#query-example) |

**Database Tables Required:**
```
1. workflows
2. workflow_steps
3. metrics_results
4. root_cause_analysis
5. mitigation_strategies
6. validation_results
7. monitoring_data
8. agent_logs
```

---

## 4. SECURITY & AUTHENTICATION
### **AMAN'S RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Security Framework** | Spring Security | 6.2.x | Authentication & authorization | `spring-boot-starter-security` | [Security Config](#security-config) |
| **JWT Tokens** | JJWT | 0.12.x | Stateless authentication | `io.jsonwebtoken:jjwt` | [JWT Example](#jwt-example) |
| **Password Encoding** | BCrypt | Built-in | Password hashing | `BCryptPasswordEncoder` | [Password Example](#password-example) |
| **API Key Management** | Spring Security | Built-in | API key validation | Custom filter | [API Key Example](#apikey-example) |
| **CORS Handling** | Spring Security | Built-in | Cross-origin requests | `@CrossOrigin` | [CORS Example](#cors-example) |

---

## 5. LOGGING & MONITORING
### **AMAN + NITYA SHARED**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Logging Framework** | SLF4J + Logback | 2.0.x | Structured logging | `spring-boot-starter-logging` | [Logging Example](#logging-example) |
| **Log Level** | Configurable | - | Control verbosity | `logback-spring.xml` | [Logback Config](#logback-config) |
| **Metrics Collection** | Micrometer | 1.12.x | Application metrics | `spring-boot-starter-actuator` | [Metrics Example](#metrics-example) |
| **Prometheus Export** | Prometheus | Latest | Metrics scraping | `micrometer-registry-prometheus` | [Prometheus Config](#prometheus-config) |
| **Centralized Logging** | ELK Stack (Optional) | Latest | Log aggregation | Docker Compose | [ELK Setup](#elk-setup) |

---

## 6. CONTAINERIZATION & ORCHESTRATION
### **AMAN'S RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Container Runtime** | Docker | 24.x | Package applications | `apt install docker.io` | [Dockerfile](#dockerfile) |
| **Container Orchestration** | Kubernetes | 1.28.x | Deploy & scale | `kubectl apply -f deployment.yaml` | [K8s Manifest](#k8s-manifest) |
| **Container Registry** | Docker Hub / ECR | - | Store images | `docker push <image>` | [Registry Config](#registry-config) |
| **Service Mesh (Optional)** | Istio | 1.19.x | Advanced traffic management | `istioctl install` | [Istio Config](#istio-config) |
| **Storage** | PersistentVolume (K8s) | - | Data persistence | StorageClass config | [PV Example](#pv-example) |

---

## 7. PYTHON AGENTS LAYER
### **NITYA'S PRIMARY RESPONSIBILITY**

| Aspect | Technology | Version | Purpose | Setup | Code Example |
|--------|-----------|---------|---------|-------|--------------|
| **Runtime** | Python | 3.10+ | Agent execution | `apt install python3.10` | N/A |
| **Package Manager** | pip | Latest | Dependency management | `pip install -r requirements.txt` | [Requirements](#python-requirements) |
| **Virtual Environment** | venv | Built-in | Isolated environment | `python -m venv venv` | [venv Setup](#venv-setup) |
| **Web Framework** | FastAPI | 0.104.x | Async HTTP server | `fastapi==0.104.1` | [FastAPI Example](#fastapi-example) |
| **ASGI Server** | Uvicorn | 0.24.x | Application server | `uvicorn==0.24.0` | [Uvicorn Config](#uvicorn-config) |
| **Messaging Client** | Kafka-Python | 2.0.x | Connect to Kafka | `kafka-python==2.0.2` | [Kafka Client](#kafka-python-client) |

---

## 8. FAIRNESS & ML LIBRARIES
### **NITYA'S RESPONSIBILITY**

### **Agent 1: Bias Detection**

| Library | Version | Purpose | Installation | Usage |
|---------|---------|---------|--------------|-------|
| **AIF360** | 0.5.0 | Fairness metrics | `pip install aif360` | [AIF360 Example](#aif360-example) |
| **scikit-learn** | 1.3.x | ML basics | `pip install scikit-learn` | [Sklearn Example](#sklearn-example) |
| **pandas** | 2.1.x | Data manipulation | `pip install pandas` | [Pandas Example](#pandas-example) |
| **numpy** | 1.24.x | Numerical computing | `pip install numpy` | [Numpy Example](#numpy-example) |
| **scipy** | 1.11.x | Statistical functions | `pip install scipy` | [Scipy Example](#scipy-example) |

### **Agent 2: Root Cause Analysis**

| Library | Version | Purpose | Installation | Usage |
|---------|---------|---------|--------------|-------|
| **SHAP** | 0.43.x | Feature importance | `pip install shap` | [SHAP Example](#shap-example) |
| **Lime** | 0.2.x | Local explanations | `pip install lime` | [LIME Example](#lime-example) |
| **Permutation Importance** | Via sklearn | Feature attribution | Built-in | [Permutation Example](#permutation-example) |
| **Matplotlib** | 3.8.x | Visualization | `pip install matplotlib` | [Plot Example](#plot-example) |
| **Seaborn** | 0.13.x | Statistical visualization | `pip install seaborn` | [Seaborn Example](#seaborn-example) |

### **Agent 3: Mitigation Strategy**

| Library | Version | Purpose | Installation | Usage |
|---------|---------|---------|--------------|-------|
| **AIF360 Algorithms** | 0.5.0 | Pre/in/post processing | `pip install aif360` | [Mitigation Example](#mitigation-example) |
| **ThresholdOptimizer** | Via AIF360 | Threshold adjustment | Included | [Threshold Example](#threshold-example) |
| **Imbalanced-learn** | 0.11.x | Resampling methods | `pip install imbalanced-learn` | [Resampling Example](#resampling-example) |
| **XGBoost** | 2.0.x | Gradient boosting | `pip install xgboost` | [XGBoost Example](#xgboost-example) |

### **Agent 4: Validation**

| Library | Version | Purpose | Installation | Usage |
|---------|---------|---------|--------------|-------|
| **AIF360** | 0.5.0 | Fairness metrics | `pip install aif360` | [Validation Example](#validation-example) |
| **pytest** | 7.4.x | Testing framework | `pip install pytest` | [pytest Example](#pytest-example) |
| **hypothesis** | 6.88.x | Property testing | `pip install hypothesis` | [Hypothesis Example](#hypothesis-example) |

### **Agent 5: Monitoring**

| Library | Version | Purpose | Installation | Usage |
|---------|---------|---------|--------------|-------|
| **Prometheus Client** | 0.18.x | Metrics export | `pip install prometheus-client` | [Prometheus Export](#prometheus-export) |
| **APScheduler** | 3.10.x | Scheduled jobs | `pip install apscheduler` | [Scheduler Example](#scheduler-example) |
| **Streaming** | Kafka-Python | Real-time events | `pip install kafka-python` | [Streaming Example](#streaming-example) |

---

# PROJECT STRUCTURE

```
agentic-fairness-system/
│
├── backend/                                    [AMAN'S DOMAIN]
│   ├── pom.xml
│   ├── src/main/java/com/fairness/
│   │   ├── FairnessApplication.java
│   │   ├── config/
│   │   │   ├── KafkaConfig.java
│   │   │   ├── SecurityConfig.java
│   │   │   ├── DatabaseConfig.java
│   │   │   └── CorsConfig.java
│   │   ├── controller/
│   │   │   ├── FairnessController.java
│   │   │   ├── AdminController.java
│   │   │   └── MonitoringController.java
│   │   ├── service/
│   │   │   ├── OrchestrationService.java
│   │   │   ├── WorkflowService.java
│   │   │   ├── KafkaProducerService.java
│   │   │   └── ResultAggregationService.java
│   │   ├── entity/
│   │   │   ├── Workflow.java
│   │   │   ├── WorkflowStep.java
│   │   │   ├── MetricsResult.java
│   │   │   ├── RootCauseAnalysis.java
│   │   │   ├── MitigationStrategy.java
│   │   │   └── ValidationResult.java
│   │   ├── repository/
│   │   │   ├── WorkflowRepository.java
│   │   │   ├── MetricsResultRepository.java
│   │   │   └── [other repos...]
│   │   ├── dto/
│   │   │   ├── FairnessRequest.java
│   │   │   ├── FairnessResponse.java
│   │   │   ├── AgentMessage.java
│   │   │   └── [other DTOs...]
│   │   ├── listener/
│   │   │   ├── BiasDetectionListener.java
│   │   │   ├── RootCauseListener.java
│   │   │   ├── MitigationListener.java
│   │   │   ├── ValidationListener.java
│   │   │   └── MonitoringListener.java
│   │   └── exception/
│   │       ├── GlobalExceptionHandler.java
│   │       └── FairnessException.java
│   │
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   ├── application-dev.yml
│   │   ├── application-prod.yml
│   │   └── logback-spring.xml
│   │
│   ├── src/test/java/
│   │   ├── controller/
│   │   ├── service/
│   │   └── integration/
│   │
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── agents/                                     [NITYA'S DOMAIN]
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── setup.py
│   │
│   ├── agent_1_bias_detection/
│   │   ├── main.py
│   │   ├── metrics_calculator.py
│   │   ├── data_loader.py
│   │   └── fairness_evaluator.py
│   │
│   ├── agent_2_root_cause/
│   │   ├── main.py
│   │   ├── feature_importance.py
│   │   ├── shap_analyzer.py
│   │   ├── proxy_detector.py
│   │   └── data_profiler.py
│   │
│   ├── agent_3_mitigation/
│   │   ├── main.py
│   │   ├── strategy_generator.py
│   │   ├── algorithm_selector.py
│   │   ├── tradeoff_analyzer.py
│   │   └── mitigators/
│   │       ├── preprocessing_mitigator.py
│   │       ├── inprocessing_mitigator.py
│   │       └── postprocessing_mitigator.py
│   │
│   ├── agent_4_validation/
│   │   ├── main.py
│   │   ├── metrics_validator.py
│   │   ├── accuracy_checker.py
│   │   └── report_generator.py
│   │
│   ├── agent_5_monitoring/
│   │   ├── main.py
│   │   ├── metrics_exporter.py
│   │   ├── alert_manager.py
│   │   ├── drift_detector.py
│   │   └── scheduler.py
│   │
│   ├── common/
│   │   ├── kafka_client.py
│   │   ├── models.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── utils.py
│   │
│   ├── tests/
│   │   ├── test_bias_detection.py
│   │   ├── test_root_cause.py
│   │   └── test_integration.py
│   │
│   └── Dockerfile
│
├── kubernetes/                                 [AMAN'S DOMAIN]
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── postgres-deployment.yaml
│   ├── kafka-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── agent-1-deployment.yaml
│   ├── agent-2-deployment.yaml
│   ├── agent-3-deployment.yaml
│   ├── agent-4-deployment.yaml
│   ├── agent-5-deployment.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   └── hpa.yaml
│
├── database/                                   [AMAN'S DOMAIN]
│   ├── migrations/
│   │   ├── V1__initial_schema.sql
│   │   ├── V2__add_metrics_table.sql
│   │   └── [more migrations...]
│   └── scripts/
│       ├── init.sql
│       └── seed.sql
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   ├── DEPLOYMENT.md
│   └── TROUBLESHOOTING.md
│
├── .github/workflows/
│   ├── ci.yml
│   ├── cd.yml
│   └── tests.yml
│
└── README.md
```

---

# COMPONENT-WISE IMPLEMENTATION

## BACKEND SETUP (AMAN)

### <a name="pomxml"></a>pom.xml - Dependencies

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.fairness</groupId>
    <artifactId>agentic-fairness-system</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    <name>Agentic AI Fairness System</name>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <kafka.version>3.6.0</kafka.version>
        <postgres.version>42.7.0</postgres.version>
        <jjwt.version>0.12.3</jjwt.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Boot Security -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Spring Kafka -->
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
        </dependency>

        <!-- PostgreSQL Driver -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>${postgres.version}</version>
            <scope>runtime</scope>
        </dependency>

        <!-- Flyway for Database Migration -->
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>

        <!-- JWT for Authentication -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>${jjwt.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>

        <!-- Actuator for Monitoring -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Micrometer Prometheus -->
        <dependency>
            <groupId>io.micrometer</groupId>
            <artifactId>micrometer-registry-prometheus</artifactId>
        </dependency>

        <!-- Lombok for Boilerplate Reduction -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### <a name="application-yml"></a>application.yml - Configuration

```yaml
spring:
  application:
    name: agentic-fairness-system
  
  # JPA/Hibernate Configuration
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
        use_sql_comments: true
    show-sql: false
    open-in-view: false
  
  # DataSource Configuration
  datasource:
    url: jdbc:postgresql://localhost:5432/fairness_db
    username: fairness_user
    password: ${DB_PASSWORD:fairness_pass}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
  
  # Kafka Configuration
  kafka:
    bootstrap-servers: localhost:9092
    
    # Producer Settings
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all
      retries: 3
      linger-ms: 10
      batch-size: 16384
    
    # Consumer Settings
    consumer:
      bootstrap-servers: localhost:9092
      group-id: fairness-consumer-group
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      auto-offset-reset: earliest
      max-poll-records: 100
      session-timeout-ms: 30000
      properties:
        spring.json.trusted.packages: "*"
  
  # Security
  security:
    user:
      name: admin
      password: ${ADMIN_PASSWORD:admin123}
  
  # Flyway Configuration
  flyway:
    locations: classpath:db/migration
    baseline-on-migrate: true
  
  # Jackson Configuration
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false
    deserialization:
      fail-on-unknown-properties: false

# Server Configuration
server:
  port: 8080
  servlet:
    context-path: /api
  compression:
    enabled: true
    min-response-size: 1024
  error:
    include-message: always
    include-binding-errors: always

# Actuator/Monitoring
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus,info,loggers
  endpoint:
    health:
      show-details: when-authorized
  metrics:
    export:
      prometheus:
        enabled: true
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true

# Logging
logging:
  level:
    root: INFO
    com.fairness: DEBUG
    org.springframework.web: INFO
    org.springframework.kafka: INFO
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/application.log
    max-size: 10MB
    max-history: 10

# JWT Configuration
jwt:
  secret: ${JWT_SECRET:your-secret-key-change-in-production-at-least-32-chars}
  expiration: 86400000  # 24 hours

# Fairness System Configuration
fairness:
  protected-attributes:
    - gender
    - race
    - age
    - disability
  fairness-threshold: 0.80
  max-workflow-steps: 5
  agent-timeout-seconds: 300
```

---

## PYTHON AGENTS SETUP (NITYA)

### <a name="python-requirements"></a>requirements.txt

```
# Core Dependencies
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Web Framework
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2

# Kafka
kafka-python==2.0.2

# Data Processing
pandas==2.1.3
numpy==1.24.3
scipy==1.11.4

# Fairness & ML
aif360==0.5.0
scikit-learn==1.3.2
imbalanced-learn==0.11.0
xgboost==2.0.2
lightgbm==4.1.1
torch==2.1.1
torchvision==0.16.1

# Model Explainability
shap==0.43.0
lime==0.2.163
matplotlib==3.8.2
seaborn==0.13.0

# Utilities
joblib==1.3.2
requests==2.31.0
python-dateutil==2.8.2

# Metrics & Monitoring
prometheus-client==0.19.0

# Scheduling
APScheduler==3.10.4

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
hypothesis==6.88.1

# Logging
python-json-logger==2.0.7

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
```

### <a name="python-setup"></a>Agent Setup Structure

```python
# agents/common/config.py
from pydantic_settings import BaseSettings
from typing import List

class KafkaConfig(BaseSettings):
    bootstrap_servers: List[str] = ["localhost:9092"]
    group_id: str = "fairness-agents"
    auto_offset_reset: str = "earliest"
    
    class Config:
        env_prefix = "KAFKA_"

class AgentConfig(BaseSettings):
    agent_name: str
    agent_id: str
    kafka_config: KafkaConfig = KafkaConfig()
    log_level: str = "INFO"
    timeout_seconds: int = 300
    
    class Config:
        env_file = ".env"

# agents/common/kafka_client.py
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import logging

class KafkaClient:
    def __init__(self, config: KafkaConfig):
        self.config = config
        self.producer = None
        self.consumer = None
        self.logger = logging.getLogger(__name__)
    
    def init_producer(self):
        """Initialize Kafka Producer"""
        self.producer = KafkaProducer(
            bootstrap_servers=self.config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
        self.logger.info("Kafka Producer initialized")
    
    def init_consumer(self, topic: str):
        """Initialize Kafka Consumer"""
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.config.bootstrap_servers,
            auto_offset_reset=self.config.auto_offset_reset,
            group_id=self.config.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            session_timeout_ms=30000
        )
        self.logger.info(f"Kafka Consumer initialized for topic: {topic}")
    
    def send_message(self, topic: str, message: dict):
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(topic, value=message)
            record_metadata = future.get(timeout=10)
            self.logger.info(f"Message sent to {topic}: {record_metadata}")
            return True
        except KafkaError as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    def consume_messages(self, topic: str, timeout: int = 60000):
        """Consume messages from Kafka topic"""
        for message in self.consumer:
            yield message.value
    
    def close(self):
        """Close connections"""
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()
```

---

## KAFKA SETUP (AMAN)

### <a name="kafka-topics"></a>Kafka Topics Creation

```bash
# Create topics using Docker Compose
docker-compose up -d kafka zookeeper

# Create topics
docker exec kafka kafka-topics.sh --create \
  --topic agent-bias-detection-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics.sh --create \
  --topic agent-root-cause-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics.sh --create \
  --topic agent-mitigation-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics.sh --create \
  --topic agent-validation-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics.sh --create \
  --topic agent-monitoring-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics.sh --create \
  --topic agent-results \
  --bootstrap-server localhost:9092 \
  --partitions 5 \
  --replication-factor 1
```

### <a name="docker-compose"></a>docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: fairness-postgres
    environment:
      POSTGRES_USER: fairness_user
      POSTGRES_PASSWORD: fairness_pass
      POSTGRES_DB: fairness_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fairness_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Zookeeper
  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    container_name: fairness-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  # Kafka
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: fairness-kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions.sh", "--bootstrap-server", "localhost:9092"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Spring Boot Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fairness-backend
    depends_on:
      postgres:
        condition: service_healthy
      kafka:
        condition: service_healthy
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/fairness_db
      SPRING_DATASOURCE_USERNAME: fairness_user
      SPRING_DATASOURCE_PASSWORD: fairness_pass
      SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka:29092
      JWT_SECRET: your-secret-key-change-in-production
      ADMIN_PASSWORD: admin123
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/actuator/health"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## DATABASE SCHEMA (AMAN)

### <a name="database-schema"></a>V1__initial_schema.sql

```sql
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
```

---

## AGENT 1: BIAS DETECTION (NITYA)

### <a name="aif360-example"></a>agent_1_bias_detection/main.py

```python
from fastapi import FastAPI
from kafka import KafkaConsumer
import json
import logging
from metrics_calculator import MetricsCalculator
from common.kafka_client import KafkaClient
from common.config import AgentConfig

app = FastAPI()
logger = logging.getLogger(__name__)
config = AgentConfig(
    agent_name="bias_detection",
    agent_id="agent-1"
)

kafka_client = KafkaClient(config.kafka_config)
metrics_calculator = MetricsCalculator()

@app.on_event("startup")
async def startup():
    kafka_client.init_producer()
    kafka_client.init_consumer("agent-bias-detection-requests")
    logger.info("Agent 1: Bias Detection started")

@app.on_event("shutdown")
async def shutdown():
    kafka_client.close()

async def process_bias_detection():
    """Listen for requests and process bias detection"""
    for message in kafka_client.consume_messages("agent-bias-detection-requests"):
        try:
            workflow_id = message['workflow_id']
            dataset_path = message['dataset_path']
            model_path = message['model_path']
            protected_attributes = message['protected_attributes']
            target_column = message['target_column']
            
            logger.info(f"Processing bias detection for workflow: {workflow_id}")
            
            # Load dataset and model
            dataset = metrics_calculator.load_dataset(dataset_path)
            model = metrics_calculator.load_model(model_path)
            
            # Compute AIF360 metrics
            metrics = metrics_calculator.compute_all_metrics(
                dataset=dataset,
                model=model,
                protected_attributes=protected_attributes,
                target_column=target_column
            )
            
            # Prepare result message
            result = {
                'workflow_id': workflow_id,
                'agent_name': 'bias_detection',
                'status': 'COMPLETED',
                'metrics': metrics,
                'timestamp': str(datetime.now())
            }
            
            # Send results to Kafka
            kafka_client.send_message('agent-results', result)
            
        except Exception as e:
            logger.error(f"Error in bias detection: {str(e)}")
            error_result = {
                'workflow_id': message.get('workflow_id'),
                'agent_name': 'bias_detection',
                'status': 'FAILED',
                'error': str(e),
                'timestamp': str(datetime.now())
            }
            kafka_client.send_message('agent-results', error_result)

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "bias_detection"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### <a name="aif360-example"></a>agent_1_bias_detection/metrics_calculator.py

```python
import pandas as pd
import numpy as np
from aif360.datasets import StandardDataset, BinaryLabelDataset
from aif360.metrics import ClassificationMetric, BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing
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
        
        # Identify feature columns
        feature_names = [col for col in df.columns 
                        if col != target_name and col not in protected_attributes]
        
        dataset = StandardDataset(
            df=df,
            label_name=target_name,
            favorable_classes=[1, 'positive', 'approved'],  # Adjust based on your data
            protected_attribute_names=protected_attributes,
            privileged_classes=privileged_groups,
            features_to_keep=feature_names
        )
        
        return dataset
    
    def compute_disparate_impact_ratio(self, y_pred: np.ndarray, protected_attr: np.ndarray,
                                       privileged_group_value) -> float:
        """
        Compute disparate impact ratio
        DI = P(Y=1|A=unprivileged) / P(Y=1|A=privileged)
        Threshold: >= 0.80 (80% rule)
        """
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
        """
        Compute equal opportunity difference (EOD)
        EOD = TPR_unprivileged - TPR_privileged
        Should be close to 0
        """
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask
        
        # True positive rate for privileged
        tpr_privileged = (y_pred[privileged_mask] == y_true[privileged_mask]).mean()
        
        # True positive rate for unprivileged
        tpr_unprivileged = (y_pred[unprivileged_mask] == y_true[unprivileged_mask]).mean()
        
        return float(tpr_unprivileged - tpr_privileged)
    
    def compute_demographic_parity(self, y_pred: np.ndarray, protected_attr: np.ndarray,
                                   privileged_group_value) -> tuple:
        """
        Demographic Parity: P(Y=1|A=a) = P(Y=1|A=a') for all a, a'
        Returns: (is_satisfied, max_difference)
        """
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask
        
        p_favorable_privileged = y_pred[privileged_mask].mean()
        p_favorable_unprivileged = y_pred[unprivileged_mask].mean()
        
        difference = abs(p_favorable_privileged - p_favorable_unprivileged)
        threshold = 0.10  # 10% difference threshold
        
        is_satisfied = difference <= threshold
        return (is_satisfied, float(difference))
    
    def compute_calibration(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                           protected_attr: np.ndarray, privileged_group_value) -> float:
        """
        Compute calibration difference
        Ensures predictions are equally accurate across groups
        """
        privileged_mask = protected_attr == privileged_group_value
        unprivileged_mask = ~privileged_mask
        
        # Calibration for privileged group
        calib_priv = np.abs(y_pred_proba[privileged_mask] - y_true[privileged_mask]).mean()
        
        # Calibration for unprivileged group
        calib_unpriv = np.abs(y_pred_proba[unprivileged_mask] - y_true[unprivileged_mask]).mean()
        
        return float(abs(calib_priv - calib_unpriv))
    
    def compute_all_metrics(self, dataset, model, protected_attributes: list,
                           target_column: str, privileged_groups: dict = None) -> dict:
        """Compute all fairness metrics"""
        
        results = {
            'disparate_impact_ratio': {},
            'equal_opportunity_difference': {},
            'demographic_parity': {},
            'calibration_difference': {},
            'affected_groups': [],
            'overall_fairness_status': 'FAIR'
        }
        
        try:
            # Get predictions
            X = dataset.drop(columns=[target_column] + protected_attributes)
            y_true = dataset[target_column].values
            y_pred = model.predict(X).astype(int)
            
            # Compute metrics for each protected attribute
            for attr in protected_attributes:
                protected_values = dataset[attr].unique()
                attr_results = {}
                
                for privilege_value in protected_values:
                    # Disparate Impact Ratio
                    di_ratio = self.compute_disparate_impact_ratio(
                        y_pred, dataset[attr].values, privilege_value
                    )
                    attr_results[f'{privilege_value}_di_ratio'] = di_ratio
                    
                    if di_ratio < 0.80:
                        results['affected_groups'].append(attr)
                        results['overall_fairness_status'] = 'BIASED'
                    
                    # Equal Opportunity Difference
                    eod = self.compute_equal_opportunity_difference(
                        y_true, y_pred, dataset[attr].values, privilege_value
                    )
                    attr_results[f'{privilege_value}_eod'] = eod
                    
                    # Demographic Parity
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
```

---

This is **PART 1** of the detailed implementation guide. Should I continue with:

1. **Agent 2: Root Cause Analysis** (Nitya) - SHAP, feature importance
2. **Agent 3: Mitigation Strategy** (Nitya) - Algorithm selection
3. **Agent 4: Validation** (Nitya) - Verification
4. **Agent 5: Monitoring** (Shared) - Continuous monitoring
5. **Spring Boot Controllers** (Aman) - REST endpoints
6. **Docker & Kubernetes** (Aman) - Deployment
7. **Database Migration Scripts** (Aman) - SQL migrations
8. **API Documentation** - Request/response examples
9. **Complete Setup Instructions** - Step-by-step guide
10. **Integration Testing** - End-to-end workflows

Which would you like me to continue with first?

**QUICK QUESTIONS FOR YOU:**

1. ✅ Is this level of detail helpful?
2. ✅ Should I add more code examples for each component?
3. ✅ Do you want version-specific configuration (dev/prod/staging)?
4. ✅ Should I include CI/CD pipeline setup (GitHub Actions)?
5. ✅ Any specific monitoring tools you prefer (ELK, Grafana, etc.)?

Let me know what to continue with!