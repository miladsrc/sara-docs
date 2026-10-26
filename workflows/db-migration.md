# Workflow — Database migration

Schema and data changes. Gates are defined in
[../architecture/OPERATING-MODEL.md](../architecture/OPERATING-MODEL.md).

**Always L3 minimum. Destructive or irreversible migrations are L4 and require
owner approval before execution.** A migration that loses data cannot be reviewed
back into existence.

Applies to PostgreSQL and Liquibase-based services in the owner's platform, and to
any project that stores state outside its process.

---

## Stages

### 1. Classify the risk before designing anything

| Operation | Risk | Requirement |
|---|---|---|
| add nullable column / new table / new index (non-blocking) | additive | L3 |
| add NOT NULL with default on a large table | rewrite/lock risk | L3 + timing plan |
| rename or retype column | breaking | L4 — expand/contract required |
| drop column / drop table / truncate | destructive | L4 + explicit approval + backup |
| data repair / backfill | correctness | L4 if it writes prod data |
| change constraint semantics | breaking | L4 |

State the classification and the affected row count (measured, not estimated)
before writing any changeset.

### 2. Inspect the real schema — G1

- Read the current definition: migration files, entity mapping, and the live
  schema. They disagree more often than anyone expects.
- Find every consumer of the column/table: do not migrate a field the code still
  writes under the old name.
- Record the schema source of truth (the migrations directory path).

**Gate:** current definition + consumer list, with paths.

### 3. Design the migration

Non-negotiable properties:

- **Idempotent-safe** or explicitly one-shot, and labelled as such.
- **Reversible**, or explicitly irreversible with the approval recorded.
- **Ordered**: added before used; removed after unused. Never a single step that
  both removes and adds the replacement.
- **No data loss** without a stated backup and a restore check.
- **Append-only changesets**: never edit an already-applied migration.

For breaking changes use **expand → migrate → contract**:

1. expand: add the new structure, dual-write, backfill
2. migrate: switch reads to the new structure, verify parity
3. contract: remove the old structure in a later, separate migration

### 4. Test on a real instance

- Apply the whole chain from empty: proves the new changeset works in sequence,
  not just in isolation.
- Apply against a copy with representative data volume: proves it does not lock
  or time out.
- Verify rollback actually runs — an untested rollback is a wish.

**Gate:** forward and rollback both executed with output recorded.

### 5. Approve — G3

L4 requires explicit owner approval of **this** migration, including the data-loss
statement. Approval of the feature is not approval of dropping a column.

### 6. Apply

- Backup or snapshot taken and its location recorded, when any destructive step is
  involved.
- Apply, then verify: schema objects exist, row counts match expectation.
- Keep the rollback command at hand and pasted in the record.

### 7. Verify and record

- Application suite against the migrated schema.
- The exact commands, in order, in the daily record.
- ADR for any breaking change: what the old shape was, the new shape, and the
  compatibility window.

## Definition of done

- [ ] risk class stated, with measured row counts
- [ ] current schema and all consumers identified
- [ ] migration is ordered, and reversible or explicitly irreversible
- [ ] applied from empty and against realistic volume
- [ ] rollback executed (or its absence explicitly approved)
- [ ] backup taken and restore path stated for destructive steps
- [ ] suite green on the migrated schema
- [ ] commands and approval recorded

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Editing an applied changeset | environments silently diverge from each other |
| Drop and add in one step | the compatibility window disappears; rollback loses data |
| `NOT NULL` with a default on a large table without measuring | table lock in production |
| Testing only on an empty database | volume is the failure mode, not correctness |
| "It's just a rename" | every consumer, serialized payload, and dashboard breaks |
| Backfill without batching | one long transaction, blocked writes, rollback by restore |
