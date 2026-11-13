-- Seed data for GGES Knowledge Graph - HT-CH-01 (Asset C_100)

-- 1. Insert Fault Nodes
INSERT INTO gges_fault_nodes (id, name, description, affected_sensors) VALUES
('CF', 'Condenser Fouling', 'Condenser fouling reduces heat-transfer efficiency by adding thermal resistance to the tubes.', ARRAY['CH-CWS-FLOW', 'CH-CON-RFT-PRES', 'CH-CON-RFT-TEMP']),
('RL', 'Refrigerant Leak', 'Refrigerant mass loss causes starvation of the evaporator, leading to low pressure and high superheat.', ARRAY['CH-EVA-RFT-PRES', 'CH-EVA-RFT-TEMP', 'CH-CON-RFT-TEMP']),
('ROC', 'Refrigerant Overcharge', 'Excess refrigerant causes condenser flooding, increasing subcooling and condensing pressure.', ARRAY['CH-CON-RFT-PRES', 'CH-CON-RFT-TEMP', 'CH-KW-COMBINED']),
('RCWF', 'Reduced Condenser Water Flow', 'Condenser water flow is reduced by pump or blockage faults, leading to poor heat rejection.', ARRAY['CH-CWS-FLOW', 'CH-CON-RFT-PRES', 'CH-CON-RFT-TEMP']),
('REWF', 'Reduced Evaporator Water Flow', 'Evaporator water flow is reduced by pump or valve faults, reducing cooling capacity.', ARRAY['CH-CHWR-FLOW', 'CH-EVA-RFT-PRES', 'CH-KW-COMBINED']),
('NC', 'Non-Condensable Gases', 'Non-condensible gases (like air) trapped in the condenser increase pressure and discharge temperature.', ARRAY['CH-CON-RFT-PRES', 'CH-CON-RFT-TEMP', 'CH-KW-COMBINED'])
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    affected_sensors = EXCLUDED.affected_sensors;

-- 2. Insert Symptom Nodes
INSERT INTO gges_symptom_nodes (id, name, sensor_id, direction, formula_logic, formula_description) VALUES
-- Direct Symptoms
('PRC_rise', 'Condenser Pressure Rise', 'C_100_2410', 1, 'z_score(CH-CON-RFT-PRES) > tau_weak', 'Rise in Condenser Refrigerant Pressure (CH-CON-RFT-PRES)'),
('PRE_drop', 'Evaporator Pressure Drop', 'C_100_2405', -1, 'z_score(CH-EVA-RFT-PRES) < -tau_weak', 'Drop in Evaporator Refrigerant Pressure (CH-EVA-RFT-PRES)'),
('TRdis_rise', 'Discharge Temperature Rise', 'C_100_2408', 1, 'z_score(CH-CON-RFT-TEMP) > tau_weak', 'Rise in Condenser Refrigerant Temperature (CH-CON-RFT-TEMP)'),
('Tsuc_rise', 'Suction Temperature Rise', 'C_100_2403', 1, 'z_score(CH-EVA-RFT-TEMP) > tau_weak', 'Rise in Evaporator Refrigerant Temperature (CH-EVA-RFT-TEMP)'),
('Tsuc_drop', 'Suction Temperature Drop', 'C_100_2403', -1, 'z_score(CH-EVA-RFT-TEMP) < -tau_weak', 'Drop in Evaporator Refrigerant Temperature (CH-EVA-RFT-TEMP)'),
('FWC_drop', 'Condenser Flow Drop', 'C_100_2029', -1, 'z_score(CH-CWS-FLOW) < -tau_weak', 'Drop in Condenser Water Flow (CH-CWS-FLOW)'),
('FWE_drop', 'Evaporator Flow Drop', 'C_100_2028', -1, 'z_score(CH-CHWR-FLOW) < -tau_weak', 'Drop in Chilled Water Flow (CH-CHWR-FLOW)'),
('kW_rise', 'Compressor Power Rise', 'C_100_2919_MD', 1, 'z_score(CH-KW-COMBINED) > tau_weak', 'Rise in Compressor Power (CH-KW-COMBINED)'),
('TRCsub_rise', 'Subcooling Rise', NULL, 1, 'z_score(CH-CON-RFT-TEMP - CH-CON-L-TEMP) > tau_weak', 'Rise in Subcooling (CH-CON-RFT-TEMP - CH-CON-L-TEMP)'),
('TRCsub_drop', 'Subcooling Drop', NULL, -1, 'z_score(CH-CON-RFT-TEMP - CH-CON-L-TEMP) < -tau_weak', 'Drop in Subcooling (CH-CON-RFT-TEMP - CH-CON-L-TEMP)'),
-- Derived Symptoms
('fdir_starve', 'Starvation Indicator', NULL, 1, 'z_score(Tsuc - (TRdis^2 + TRCsub^2)) > 0', 'Positive fdir: High Suction Temp relative to High-Side (Starvation)'),
('fdir_flood', 'Flooding Indicator', NULL, -1, 'z_score(Tsuc - (TRdis^2 + TRCsub^2)) < 0', 'Negative fdir: Low Suction Temp relative to High-Side (Flooding)'),
('Qbal_error', 'Energy Balance Error', NULL, 1, 'abs(Q_evap + kW - Q_cond) > threshold', 'Significant deviation in Chiller Heat Balance (Q_evap + kW - Q_cond)'),
('PRC_TRC_coupling', 'Pressure-Subcooling Coupling', NULL, 1, 'z_score(PRC * TRCsub) > tau_weak', 'Strong coupling between pressure and subcooling (ROC/NC indicator)')
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    sensor_id = EXCLUDED.sensor_id,
    direction = EXCLUDED.direction,
    formula_logic = EXCLUDED.formula_logic,
    formula_description = EXCLUDED.formula_description;

-- 3. Insert Edges (Diagnostic Logic)
INSERT INTO gges_edges (fault_id, symptom_id, relation_type, weight) VALUES
-- NC (Non-Condensable Gases)
('NC', 'PRC_rise', 'indicates', 8.0),
('NC', 'TRdis_rise', 'indicates', 8.0),
('NC', 'TRdis_rise', 'distinguishes', 1.0),
('NC', 'TRCsub_rise', 'indicates', 6.0),
('NC', 'fdir_flood', 'indicates', 4.0),

-- ROC (Refrigerant Overcharge)
('ROC', 'PRC_rise', 'indicates', 8.0),
('ROC', 'TRCsub_rise', 'indicates', 8.0),
('ROC', 'fdir_flood', 'indicates', 6.0),

-- RCWF (Reduced Condenser Water Flow)
('RCWF', 'FWC_drop', 'indicates', 10.0),
('RCWF', 'FWC_drop', 'distinguishes', 1.0),
('RCWF', 'PRC_rise', 'indicates', 7.0),
('RCWF', 'TRdis_rise', 'indicates', 6.0),

-- REWF (Reduced Evaporator Water Flow)
('REWF', 'FWE_drop', 'indicates', 10.0),
('REWF', 'FWE_drop', 'distinguishes', 1.0),
('REWF', 'PRE_drop', 'indicates', 6.0),
('REWF', 'kW_rise', 'indicates', 4.0),

-- CF (Condenser Fouling)
('CF', 'FWC_drop', 'indicates', 7.0),
('CF', 'PRC_rise', 'indicates', 8.0),
('CF', 'TRdis_rise', 'indicates', 7.0),
('CF', 'Qbal_error', 'indicates', 8.0),

-- RL (Refrigerant Leak)
('RL', 'PRE_drop', 'indicates', 10.0),
('RL', 'Tsuc_rise', 'indicates', 8.0),
('RL', 'Tsuc_rise', 'distinguishes', 1.0),
('RL', 'TRCsub_drop', 'indicates', 8.0),
('RL', 'fdir_starve', 'indicates', 6.0)
ON CONFLICT (fault_id, symptom_id, relation_type) DO UPDATE SET 
    weight = EXCLUDED.weight;
