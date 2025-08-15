# Contributing to LastWish.eth

Thank you for your interest in contributing to LastWish.eth! This document provides guidelines for contributing to this decentralized will creation platform.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/lastwish-eth.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes locally
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

1. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

2. Get your API keys:
   - **Moralis API Key**: Sign up at [moralis.io](https://moralis.io/)
   - **WalletConnect Project ID**: Create a project at [cloud.walletconnect.com](https://cloud.walletconnect.com/)

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:8000`

## Code Style

- Use consistent indentation (2 spaces)
- Follow existing naming conventions
- Add comments for complex logic
- Keep functions small and focused
- Use meaningful variable names

## Testing

- Test all wallet connection functionality
- Verify ENS resolution works correctly
- Test asset loading and assignment features
- Ensure responsive design works on mobile devices
- Test payment flow (use testnet for development)

## Security Considerations

- Never commit API keys or private keys
- Validate all user inputs
- Use secure random number generation
- Follow web3 security best practices
- Test thoroughly before deploying

## Pull Request Guidelines

- Provide a clear description of changes
- Include screenshots for UI changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed

## Reporting Issues

- Use the GitHub issue tracker
- Provide detailed reproduction steps
- Include browser and wallet information
- Add screenshots or videos if helpful

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional tone

## Questions?

Feel free to open an issue for questions or join our community discussions.

Thank you for contributing to the decentralized future of digital inheritance!

