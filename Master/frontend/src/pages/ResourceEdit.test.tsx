import { render, } from '../utils/test';
import { ResourceEdit, } from './ResourceEdit';

vi.mock('@refinedev/antd', async () => ({
    ...(await vi.importActual('@refinedev/antd')),
    Edit          : ({
        children,
        ...props
    } : any) => (
        <div data-testid='edit'>
            {props.headerButtons}
            {props.title}
            {children}
        </div>
    ),
    RefreshButton : (props : any) => (
        <button aria-label={props['aria-label'] || 'refresh'}>refresh</button>
    ),
    useForm       : () => ({
        form      : {
            getFieldValue : () => undefined,
        },
        formProps : {},
    }),
}));

vi.mock('antd', async () => ({
    ...(await vi.importActual('antd')),
    Form : (props : any) => (
        <form data-testid='form-layout'>{props.children}</form>
    ),
}));

describe('<ResourceEdit />', () => {
    it('renders edit mode with header buttons', () => {
        const { getByText, } = render(
            <ResourceEdit resource='test'>
                {() => <div>EditContent</div>}
            </ResourceEdit>
        );

        expect(getByText('refresh')).toBeInTheDocument();
    });
});
