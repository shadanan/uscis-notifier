# Send Pushover Notification when USCIS Receipt Date is Updated

This repo contains a GitHub action that sends pushover notifications when USCIS
updates the receipt date on their [website](https://egov.uscis.gov/processing-times/).

## Pseudocode

```
- retrieve the receipt date for a case inquiry from USCIS processing times web site
- read the previous receipt date from disk
- compare the previous receipt date with current receipt date
- if they are different, then:
  - send a notification
  - update the previous receipt date with the current receipt date
```
