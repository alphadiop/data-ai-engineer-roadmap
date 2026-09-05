### Ton architecture finale
```` text
                    PipelineLogger
                          │
                          ▼
                 load_config()
                          │
              ┌───────────┴───────────┐
              │                       │
          local                  databricks
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                    path_logs
                          │
                          ▼
                   get_path_logs()
                          │
                          ▼
                self.path_log
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
             Console          FileHandler
                 │                 │
                 │                 ▼
                 │        202501_....log
                 │                 │
                 └────────┬────────┘
                          ▼
                       finalize()
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
                .ok              .nook
````