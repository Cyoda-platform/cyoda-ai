flowchart TD
    A[None] --> B[ingest_data_process]
    B --> C[data_ingested]
    C --> D[aggregate_raw_data]
    D --> E[data_aggregated]
    E --> F[generate_report_process]
    F --> G[report_sent]

    classDef automated fill:#ffcc00,stroke:#ffcc00;
    classDef manual fill:#ffffff,stroke:#000000;

    class A,B,C,D,E,F automated;
    class G manual;
