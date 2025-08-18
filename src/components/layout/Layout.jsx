import React from 'react';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <Navbar />

      <main className="p-4 sm:p-6 lg:p-8">
        <div className="bg-yellow-400 text-yellow-900 p-4 rounded-md mb-6 text-center font-semibold">
          WARNING: NEVER enter private keys, seed phrases, or passwords. Store them separately in a secure location.
        </div>
        {children}
      </main>

      {/* Footer placeholder */}
      <footer className="bg-gray-800 p-4 text-center text-sm text-gray-400">
        <p>&copy; {new Date().getFullYear()} LastWish.eth. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
