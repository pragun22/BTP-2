import React from 'react';
import './header.less';

function Header (props) {
  return (
    <header className="header flex-box">
      <i className="header-icon fas fa-cloud-sun-rain"></i><span className="header-title">Flood Prediction</span>
      <div className="author">made for BTP-2</div>
    </header>
  )
}

export default Header;
