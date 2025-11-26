import { render, } from '../utils/test';
import { ResourceShow, } from './ResourceShow';

const useShowData : Record<string, any> = {
    query : {},
};

vi.mock('@refinedev/antd', async () => ({
    ...(await vi.importActual('@refinedev/antd')),
    Show          : ({
        children,
        ...props
    } : any) => (
        <div data-testid='show'>
            {children}
            {props.title}
            {props.headerButtons}
        </div>
    ),
    RefreshButton : (props : any) => (
        <button aria-label={props['aria-label'] || 'refresh'}>refresh</button>
    ),
    EditButton    : (props : any) => (
        <button aria-label={props['aria-label'] || 'edit'}>edit</button>
    ),
    useForm       : () => ({
        form      : {},
        formProps : {},
    }),
}));

vi.mock('@refinedev/core', () => ({
    useShow : () => useShowData,
    useGo   : () => vi.fn(),
}));

vi.mock('antd', async () => ({
    ...(await vi.importActual('antd')),
    Form : (props : any) => (
        <form data-testid='form-layout'>{props.children}</form>
    ),
}));

describe('<ResourceShow />', () => {
    beforeEach(() => {
        useShowData.query.data = {
            data : {
                id   : 1,
                name : 'Test',
            },
        };

        useShowData.query.isLoading = false;
    });

    it('renders title, header buttons, and children when data is present', () => {
        const { getByTestId, getByText, } = render(
            <ResourceShow resource='test'>
                {() => <div>ChildContent</div>}
            </ResourceShow>
        );

        expect(getByTestId('show')).toBeInTheDocument();
        expect(getByText('resources.test.details')).toBeInTheDocument();
        expect(getByText('refresh')).toBeInTheDocument();
        expect(getByText('edit')).toBeInTheDocument();
        expect(getByTestId('form-layout')).toBeInTheDocument();
        expect(getByText('ChildContent')).toBeInTheDocument();
    });

    it('does not render FormLayout if no data', () => {
        useShowData.query = {
            data      : undefined,
            isLoading : false,
        };

        const { queryByTestId, } = render(
            <ResourceShow resource='test'>
                {() => <div>ChildContent</div>}
            </ResourceShow>
        );

        expect(queryByTestId('form-layout')).not.toBeInTheDocument();
    });
});
