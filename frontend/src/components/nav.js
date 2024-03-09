import React from 'react';
import { styled, Button, AppBar, Toolbar } from '@mui/material/';
import logo from '../images/Logo.svg';
import { NavLink } from 'react-router-dom';

function Nav() {

    const CustomizedAppBar = styled(AppBar)`
background: #fff; 
color: #7E5F50;
`;

    const CustomizedAppBarMenuItem = styled(Button)`
font-size:0.95rem; 
padding-right:2%;
padding-left:2%;
`;

    return (
        <CustomizedAppBar>
            <Toolbar>
                <img src={logo} className="logo" alt="logo" style={{ width: '18%', paddingRight: '2%', paddingLeft: '2%' }} />
                {/*Change width of #menuItem to control the position of menu items*/}
                <div id="menuItem" style={{ marginLeft: 'auto', width: '55%' }}>
                    <CustomizedAppBarMenuItem>Mock interview</CustomizedAppBarMenuItem>
                    <NavLink><CustomizedAppBarMenuItem>Career Path Builder</CustomizedAppBarMenuItem></NavLink>
                    <CustomizedAppBarMenuItem>Smart Tracking</CustomizedAppBarMenuItem>
                    <Button sx={{ marginLeft: '2%', fontSize: '0.8rem' }} color="primary" variant="contained">Login</Button>
                </div>
            </Toolbar>
        </CustomizedAppBar>
    );
}

export default Nav;

