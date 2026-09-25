---
type: index
tags: [index, deployment, infrastructure]
---
# Deployment & Infrastructure Index

- [[Docker Compose Local Stack]] — the four local containers
- [[Render Backend Service]] · [[PayMongo Setup]] — production container (nginx + PHP + Reverb + queue + scheduler)
- [[Frontend Hosting]] — Render static site (and the Vercel config)
- [[NeonDB]] — production PostgreSQL with pooler/direct hosts
- [[Render Persistent Disk]] — uploads storage
- [[Release Workflow]] — how code reaches production and how to roll back
- [[Go-Live Checklist]] — owner actions before launch
- [[Mobile Release Build]] — signed Android APK

```mermaid
flowchart LR
  dev[Developer on WSL] -->|git push main| GHB[GitHub skillserve-web-backend]
  dev -->|git push main| GHF[GitHub skillserve-web-frontend]
  GHB -->|auto-deploy| RB[Render Docker web service<br/>Dockerfile.render]
  GHF -->|auto-deploy| RF["Render static site<br/>npm install, npm run build → dist"]
  RB --> NEON[(NeonDB)]
  RB --> DISK[(Render disk /var/www/html/storage/app)]
  dev -->|flutter build apk --release| APK[Signed APK com.skillserve.mobile]
  APK --> RB
  RF --> RB
```

Source doc: root `DEPLOYMENT.md`. Back to [[Home]]
