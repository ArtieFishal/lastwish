# Contributing to LastWish.eth

Thank you for your interest in contributing to LastWish.eth! This document provides guidelines for contributing to this decentralized will creation platform.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for all contributors

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template when available
3. Provide clear reproduction steps
4. Include browser and wallet information

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly across different browsers and wallets
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

1. Clone your fork
2. Copy `.env.example` to `.env` and configure API keys
3. Start local server: `npm start`
4. Open `http://localhost:8000`

### Testing Guidelines

- Test wallet connections (MetaMask, WalletConnect)
- Verify asset loading functionality
- Test beneficiary management
- Ensure payment flow works on testnet
- Check responsive design on mobile devices

### Code Style

- Use consistent indentation (2 spaces)
- Follow existing naming conventions
- Add comments for complex logic
- Keep functions small and focused

### Security Considerations

- Never commit API keys or sensitive data
- Validate all user inputs
- Follow Web3 security best practices
- Test transaction flows thoroughly

## Areas for Contribution

### High Priority
- Multi-chain support (Polygon, BSC, Arbitrum)
- Enhanced mobile experience
- Accessibility improvements
- Performance optimizations

### Medium Priority
- Additional wallet integrations
- Advanced asset management features
- Improved error handling
- Documentation improvements

### Low Priority
- UI/UX enhancements
- Additional language support
- Analytics integration
- Social features

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] Changes are tested across multiple browsers
- [ ] Documentation is updated if needed
- [ ] No console errors or warnings
- [ ] Responsive design is maintained

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Manual testing completed
- [ ] Cross-browser testing done
- [ ] Mobile testing completed
- [ ] Wallet integration tested

## Screenshots
Include screenshots for UI changes
```

## Getting Help

- Join our community discussions
- Check the documentation in `/docs`
- Review existing issues and PRs
- Ask questions in issue comments

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Community acknowledgments

Thank you for helping make LastWish.eth better for everyone!

