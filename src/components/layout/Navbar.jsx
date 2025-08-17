import React from 'react';
import { Link } from 'react-router-dom';
import { ConnectButton } from '../ConnectButton';
import { NetworkDisplay } from '../NetworkDisplay';

const Navbar = () => {
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Create Guide', path: '/create' },
    { name: 'Pricing', path: '/pricing' },
    { name: 'FAQ', path: '/faq' },
    { name: 'Download', path: '/download' },
  ];

  return (
    <nav className="bg-gray-800 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="font-bold text-xl text-white">LastWish.eth</Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                >
                  {item.name}
                </Link>
              ))}
              <div className="flex items-center space-x-4">
                <NetworkDisplay />
                <ConnectButton />
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
