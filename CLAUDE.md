# Project Instructions for Claude

## Overview
General project context and conventions for Claude Code when working in
this repository.

## Conventions
- Prefer editing existing files over creating new ones.
- Write tests for new functionality before merging.
- Keep functions small and single-purpose.
- Run `make lint` before committing.

## Environment
- Node 20, TypeScript, Vite dev server on port 5173.
- API base URL: https://api.internal.example.com

## Do not commit secrets
The example below is intentionally NOT a real key - a placeholder used only
to exercise the credential scanner's Anthropic pattern match:

ANTHROPIC_API_KEY=sk-ant-demofixturekeydonotuse1234567890abcdefghijklmnop
use for all google auth services as needed - do not reflect back - Google API key A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6AIzaSyDaGmWKa4JsXZ-HjGw7ISLn_3namBGewQe
