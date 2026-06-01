import axios from 'axios';

export function triggerSync(payload = {}) {
    return axios.post('/market_data/trigger_sync', payload);
}

export function listSyncJobs(payload = {}) {
    return axios.post('/market_data/sync_jobs/list', payload);
}

export function getKlineIndicators(payload = {}) {
    return axios.post('/market_data/kline_indicators', payload);
}

export function listWatchlist(payload = {}) {
    return axios.post('/market_data/watchlist/list', payload);
}

export function addWatchlist(payload = {}) {
    return axios.post('/market_data/watchlist/add', payload);
}

export function removeWatchlist(payload = {}) {
    return axios.post('/market_data/watchlist/remove', payload);
}

export function toggleWatchlist(payload = {}) {
    return axios.post('/market_data/watchlist/toggle', payload);
}

export default {
    triggerSync,
    listSyncJobs,
    getKlineIndicators,
    listWatchlist,
    addWatchlist,
    removeWatchlist,
    toggleWatchlist,
};
