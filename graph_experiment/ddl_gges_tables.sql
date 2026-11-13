-- DDL for Chiller Graph-Grounded Evidence Scoring (GGES) Knowledge Graph
-- Schema: sgp7_dev

-- Fault Nodes Table
CREATE TABLE IF NOT EXISTS sgp7_dev.gges_fault_nodes (
    id VARCHAR(50) PRIMARY KEY, -- e.g., 'NC', 'ROC', 'CF'
    name VARCHAR(100) NOT NULL,
    description TEXT,
    affected_sensors TEXT[] -- Array of sensor names involved in identifying this fault
);

-- Symptom Nodes Table
CREATE TABLE IF NOT EXISTS sgp7_dev.gges_symptom_nodes (
    id VARCHAR(50) PRIMARY KEY, -- e.g., 'PRC_rise', 'FWC_drop'
    name VARCHAR(100) NOT NULL,
    sensor_id VARCHAR(50), -- Mapping to sensor_master.sensor_id for HT-CH-01 (C_100)
    direction INTEGER CHECK (direction IN (1, -1)), -- +1 for rise, -1 for drop
    formula_logic TEXT, -- Formula or logic for activation
    formula_description TEXT -- Human-readable formula using sensor names instead of IDs
);

-- Edges Table (Many-to-Many Relationship between Faults and Symptoms)
CREATE TABLE IF NOT EXISTS sgp7_dev.gges_edges (
    fault_id VARCHAR(50) REFERENCES sgp7_dev.gges_fault_nodes(id),
    symptom_id VARCHAR(50) REFERENCES sgp7_dev.gges_symptom_nodes(id),
    relation_type VARCHAR(20) CHECK (relation_type IN ('indicates', 'distinguishes')),
    weight DOUBLE PRECISION DEFAULT 1.0, -- Expert weight (w0)
    PRIMARY KEY (fault_id, symptom_id, relation_type)
);
