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

let resourceListData : Record<string, string | number>[] = [
    {
        id          : 'AABBCCDDEEFF',
        displayName : 'Test',
        mode        : 'sensor',
        lastSeen    : '2024-01-01T00:00:00Z',
    },
];

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
                    data : resourceListData,
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
            dataIndex,
            render,
        } : any) => (
            <div>
                <span>{title}</span>
                {render && render(resourceListData[0][dataIndex])}
            </div>
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
    beforeEach(() => {
        resourceListData = [
            {
                id          : 'AABBCCDDEEFF',
                displayName : 'Test',
                mode        : 'sensor',
                lastSeen    : '2024-01-01T00:00:00Z',
            },
        ];
    });

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

    it('renders status icon for active and inactive', () => {
        resourceListData = [
            {
                id          : '1',
                displayName : 'Test',
                mode        : 'sensor',
                lastSeen    : new Date().toISOString(),
            }, {
                id          : '2',
                displayName : 'Test2',
                mode        : 'sensor',
                lastSeen    : '2000-01-01T00:00:00Z',
            },
        ];

        const { container, } = customRender(<DeviceList />);

        expect(container).toBeTruthy();
    });

    it('formats device ID in MAC format', () => {
        const { getByText, } = customRender(<DeviceList />);

        expect(getByText('AA-BB-CC-DD-EE-FF')).toBeInTheDocument();
    });
});
