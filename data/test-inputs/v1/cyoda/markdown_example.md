stateDiagram-v2
    [*] --> None
    None --> data_ingested : Automated Transition
    data_ingested --> data_aggregated : Automated Transition
    data_aggregated --> report_sent : Automated Transition

    state data_ingested {
        [*] --> ingest_data_process : Process
    }

    state data_aggregated {
        [*] --> aggregate_raw_data : Process
    }

    state report_sent {
        [*] --> generate_report_process : Process
    }
    
    None : Manual Transition
    data_ingested : Manual Transition
    data_aggregated : Manual Transition
    report_sent : Manual Transition
