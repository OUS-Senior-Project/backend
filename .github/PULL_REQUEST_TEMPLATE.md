# Pull Request Template

## 📌 Summary

Provide a short, clear explanation of the backend changes made in this PR.

---

## 🎟️ Related Jira Ticket

Include the required Jira ticket ID and link:

- Ticket: [PROJ-###](https://your-jira-url/browse/PROJ-###)

---

## 🛠️ What’s Changed?

Describe backend updates such as:

- New/updated API endpoints  
- Database changes or migrations  
- Bug fixes  
- Refactoring  
- Performance improvements  

---

## 🧪 How to Test

Steps to manually validate:

1. Run backend (`uvicorn app.main:app --reload`)
2. Call endpoint: `GET /api/...`
3. Expected result:
4. Include example payloads if useful:

```json
{
  "example": "payload"
}
