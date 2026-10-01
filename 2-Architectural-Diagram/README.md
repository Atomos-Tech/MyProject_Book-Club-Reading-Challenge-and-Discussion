# Architectural Diagram

This folder describes the proposed logical architecture for the Book Club Reading Challenge and Discussion Portal.

- [Book_Club_Architecture.svg](Book_Club_Architecture.svg) — submission-ready architectural diagram.
- [Architecture_Overview.md](Architecture_Overview.md) — component responsibilities, data flow, and quality-attribute decisions.

The design uses a layered modular architecture. A browser-based client calls a single application API. The API delegates work to focused services and persists records in a relational database. Authentication and authorization guard all protected operations, while monitoring and backup support availability and recovery.

