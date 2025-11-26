import { API_ENDPOINT, } from '../constants';
import { dataProvider, } from './dataProvider';

describe('dataProvider', () => {
    beforeEach(() => {
        fetchMock.resetMocks();
    });

    it('getList', async () => {
        fetchMock.mockResponseOnce(JSON.stringify([
            {
                id   : 1,
                name : 'Test',
            },
        ]));

        const result = await dataProvider.getList({
            resource   : 'test',
            pagination : {
                currentPage : 1,
                pageSize    : 10,
            },
        });

        expect(result.data).toEqual([
            {
                id   : 1,
                name : 'Test',
            },
        ]);

        expect(result.total).toBe(1);
        expect(fetchMock).toHaveBeenCalledWith(`${API_ENDPOINT}/test?limit=10&offset=0`);
    });

    it('getOne', async () => {
        fetchMock.mockResponseOnce(JSON.stringify({
            id   : 1,
            name : 'Test',
        }));

        const result = await dataProvider.getOne({
            resource : 'test',
            id       : 1,
        });

        expect(result.data).toEqual({
            id   : 1,
            name : 'Test',
        });

        expect(fetchMock).toHaveBeenCalledWith(`${API_ENDPOINT}/test/1`);
    });

    it('update', async () => {
        fetchMock.mockResponseOnce(JSON.stringify({
            id   : 1,
            name : 'Test Updated',
        }));

        const result = await dataProvider.update({
            resource  : 'test',
            id        : 1,
            variables : {
                name : 'Test Updated',
            },
        });

        expect(result.data).toEqual({
            id   : 1,
            name : 'Test Updated',
        });

        expect(fetchMock).toHaveBeenCalledWith(`${API_ENDPOINT}/test/1`, expect.any(Object));
    });

    it('deleteOne', async () => {
        fetchMock.mockResponseOnce(JSON.stringify({
            id   : 1,
            name : 'Test',
        }));

        const result = await dataProvider.deleteOne({
            resource : 'test',
            id       : 1,
        });

        expect(result.data).toEqual({
            id   : 1,
            name : 'Test',
        });

        expect(fetchMock).toHaveBeenCalledWith(`${API_ENDPOINT}/test/1`, expect.any(Object));
    });
});
