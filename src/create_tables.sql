DROP TABLE IF EXISTS public.machines CASCADE;
CREATE TABLE public.machines (
    machineId VARCHAR(10) PRIMARY KEY,
    machineType VARCHAR(50) NOT NULL,
    purchaseDate DATE NOT NULL,
    operationalCost DECIMAL(10, 2) NOT NULL
);

DROP TABLE IF EXISTS public.operators CASCADE;
CREATE TABLE public.operators (
    operatorId VARCHAR(10) PRIMARY KEY,
    machineId VARCHAR(10) NOT NULL REFERENCES public.machines(machineId),
    operatorName VARCHAR(100) NOT NULL,
    workShift VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS public.incidents CASCADE;
CREATE TABLE public.incidents (
    incidentId VARCHAR(10) PRIMARY KEY,
    machineId VARCHAR(10) NOT NULL REFERENCES public.machines(machineId),
    machineType VARCHAR(50) NOT NULL,
    incidentType VARCHAR(50) NOT NULL,
    incidentDate DATE NOT NULL,
    severity VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS public.maintenances CASCADE;
CREATE TABLE public.maintenances (
    maintenanceId VARCHAR(10) PRIMARY KEY,
    machineId VARCHAR(10) NOT NULL REFERENCES public.machines(machineId),
    maintenanceDate DATE,
    maintenanceCost DECIMAL(10, 2),
    severity VARCHAR(20) NOT NULL,
    downtime INTEGER NOT NULL
);