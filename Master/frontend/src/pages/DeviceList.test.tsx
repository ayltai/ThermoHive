import { render as customRender, } from '../utils/test';
import { DeviceList, } from './DeviceList';

const mockList   = vi.fn();
const mockShow   = vi.fn();

vi.mock('@refinedev/core', () => ({
    useList       : () => ({
        data : {
            data : [],
        },
    }),
    useNavigation : () => ({
        list : mockList,
        show : mockShow,
    }),
}));

fetchMock.mockResponseOnce(JSON.stringify({
    ok   : true,
    json : () => Promise.resolve([
        1,
    ]),
}));

vi.mock('./ResourceList', () => ({
    ResourceList : ({
        children,
    } : any) => (
        <div data-testid='resource-list'>
            {children({
                isLoading : false,
                isSuccess : true,
                sorters   : [],
                data      : {
                    data : [
                        {
                            id          : 1,
                            displayName : 'Test',
                            mode        : 'sensor',
                            lastSeen    : '2024-01-01T00:00:00Z',
                        },
                    ],
                },
            })}
        </div>
    ),
}));

vi.mock('antd', async () => ({
    ...(await vi.importActual('antd')),
    Button : (props : any) => (
        <button {...props}>
            {props.children}
        </button>
    ),
    Table  : {
        Column: ({
            title,
        } : any) => (
            <>
                <div>
                    <span>{title}</span>
                </div>
            </>
        ),
    },
    Tag    : ({
        children,
    } : any) => (
        <span>
            {children}
        </span>
    ),
}));

describe('<DeviceList />', () => {
    it('renders displayName column', () => {
        const { getByText, } = customRender(<DeviceList />);

        expect(getByText('labels.device.displayName')).toBeInTheDocument();
    });

    it('renders mode column', () => {
        const { getByText, } = customRender(<DeviceList />);

        expect(getByText('labels.device.mode')).toBeInTheDocument();
    });

    it('renders lastSeen column', () => {
        const { getByText, } = customRender(<DeviceList />);

        expect(getByText('labels.device.lastSeen')).toBeInTheDocument();
    });
});
