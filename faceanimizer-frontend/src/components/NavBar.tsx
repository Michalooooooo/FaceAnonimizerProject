import { AppShell, Burger, Button } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link } from 'react-router-dom';

function NavBar() {

    return (
        <AppShell header={{ height: 50 }}>
            <AppShell.Header>
                <Button className='home-button'>
                    <Link to="/">Home page</Link>
                </Button>
                <Button className='processing-button'>
                    <Link to="/processing">Processing</Link>
                </Button>
            </AppShell.Header>
        </AppShell>

    );
}

export default NavBar