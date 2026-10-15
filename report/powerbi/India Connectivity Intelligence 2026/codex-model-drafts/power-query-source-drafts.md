# Power Query source drafts

Replace `<REPOSITORY_ROOT>` with the local repository folder in Power BI Desktop. Import the six CSV tables; set `period_end` to Date type and `value` to Decimal Number. Preserve `source_page`, `source_url`, `unit`, and `scope_note`.

```powerquery
let
    RepositoryRoot = "<REPOSITORY_ROOT>",
    Source = Csv.Document(File.Contents(RepositoryRoot & "\data\processed\fact_connectivity.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    PromotedHeaders
```

Use the same pattern for `dim_period.csv`, `dim_geography.csv`, `dim_provider.csv`, `dim_metric.csv`, and `dim_source.csv` by replacing the filename above.

All file connections are draft-only. Do not publish local file paths or credentials in the repository.
