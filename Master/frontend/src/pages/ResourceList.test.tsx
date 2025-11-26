import { render, } from '../utils/test';
import { ResourceList, } from './ResourceList';

const mockMutate = vi.fn();

vi.mock('@refinedev/antd', async () => ({
    ...(await vi.importActual('@refinedev/antd')),
    useTable : () => ({
        sorters    : [],
        tableQuery : {
            data      : {
                data  : [
                    {
                        id   : 1,
                        name : 'Test',
                    },
                ],
                total : 1,
            },
            isLoading : false,
            isSuccess : true,
        },
        tableProps : {
            pagination : {},
        },
    }),
}));

vi.mock('@refinedev/core', () => ({
    useDeleteMany : () => ({
        mutate : mockMutate,
    }),
}));

describe('<ResourceList />', () => {
    it('renders with children', () => {
        const { getByText, } = render(
            <ResourceList resource='test'>
                {() => <div>ChildContent</div>}
            </ResourceList>
        );

        expect(getByText('resources.test')).toBeInTheDocument();
    });
});
