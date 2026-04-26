# Reset Checklist

Use this checklist when executing Path C (force reset).

## Pre-Reset

- [ ] User explicitly passed `reset` or `--force` argument
- [ ] Count and note the number of entity pages to be deleted (for the confirmation message)
- [ ] Note any topics that will be lost (from index.md) to include in confirmation

## Deletion

- [ ] Delete all `.md` files in `wiki/` **except** `index.md` and `log.md`
- [ ] Verify `index.md` and `log.md` still exist after deletion

## Template Reset

- [ ] Overwrite `wiki/index.md` with empty-index-template.md content
- [ ] Overwrite `wiki/log.md` with empty-log-template.md content
- [ ] Replace `YYYY-MM-DD` in index.md with today's date

## Confirmation

- [ ] Report: "Wiki reset complete. [N] pages removed."
- [ ] Prompt: "Run `/compile-papers` with your source material to begin."

## Safety Rules

- NEVER delete `index.md` or `log.md` — only overwrite them with clean templates
- NEVER proceed with reset unless the argument is explicitly `reset` or `--force`
- If uncertain which files are entity pages vs structural files, list them and confirm with the user
