# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of the Hyper-Local Dhaka PM2.5 STGCN project very seriously. 

If you discover a vulnerability, please do NOT open a public issue. Instead, please follow these steps:
1. Email your findings to the security team at security@dhaka-pm25-stgcn.local (placeholder email).
2. Provide a detailed description of the vulnerability, including steps to reproduce.
3. We will acknowledge receipt of your vulnerability report within 48 hours and provide an estimated timeline for a patch.

## Best Practices
- Keep your `.env` file secure and never commit it to version control.
- Ensure all API keys (Google Maps, OpenAQ) are restricted by IP or domain.
- Use strong, randomly generated keys for JWT authentication.
