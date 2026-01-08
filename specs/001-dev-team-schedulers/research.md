# Research: Storage Mechanism for Automation Tool

## Decision

For storing the application's configuration and the on-call schedule, we will use a single JSON file (`config.json`) hosted in a private Google Cloud Storage (GCS) bucket.

## Rationale

This approach was chosen for its simplicity and alignment with the project's "MVP & Simplicity" principle.

- **Simplicity**: Using a single JSON file in GCS is the most straightforward method for persisting configuration data. It requires minimal setup and the access logic in the FastAPI backend is simple (read the file on startup, write the file when changes are made via the admin UI).
- **Cost-Effective**: GCS is very inexpensive for the small amount of data we need to store.
- **Sufficient for MVP**: The application's data is not complex. We do not need the querying capabilities of a full database like Cloud SQL or Firestore. The risk of concurrent writes is negligible given the expected usage (a few admins).

This solution provides a simple, robust, and cost-effective way to manage configuration for the MVP. If the application's needs grow in complexity, we can migrate to a more sophisticated solution like Firestore in the future.

## Alternatives Considered

- **Cloud SQL**: A fully-managed relational database. This was rejected as it introduces unnecessary complexity and cost for the simple, non-relational data we need to store.
- **Firestore**: A NoSQL document database. This was a strong contender and would be a good next step if the data model becomes more complex. However, for the initial MVP, the overhead of setting up Firestore is not justified compared to a simple GCS file.
