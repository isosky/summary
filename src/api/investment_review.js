import axios from 'axios';

const authToken = 'serveraly'; // dev token matching backend g_tokens

function authHeader() {
    return { headers: { Authorization: `Token ${authToken}` } };
}

export function queryList(payload = {}) {
    return axios.post('/query_investment_review_plan_list', payload, authHeader());
}

export function getDetail(payload = {}) {
    return axios.post('/get_investment_review_plan_detail', payload, authHeader());
}

export function saveBundle(payload = {}) {
    return axios.post('/save_investment_review_plan_bundle', payload, authHeader());
}

export function saveModification(payload = {}) {
    return axios.post('/save_investment_review_modification', payload, authHeader());
}

export function saveExecution(payload = {}) {
    return axios.post('/save_investment_review_execution', payload, authHeader());
}

export function saveReview(payload = {}) {
    return axios.post('/save_investment_review_review', payload, authHeader());
}

export default {
    queryList,
    getDetail,
    saveBundle,
    saveModification,
    saveExecution,
    saveReview,
};
