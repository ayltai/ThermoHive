import { render, } from '@testing-library/react';
import type { ReactNode, } from 'react';
import { MemoryRouter, } from 'react-router';

const customRender = (ui : any, {
    ...rest
} : {
    [ key : string] : any,
} = {}) => render(ui, {
    wrapper : ({
        children,
    } : {
        children : ReactNode,
    }) => (
        <MemoryRouter>
            {children}
        </MemoryRouter>
    ),
    ...rest,
});

export * from '@testing-library/react';

export { customRender as render, };
