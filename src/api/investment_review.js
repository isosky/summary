import axios from 'axios';

export function queryList(payload = {}) {
    return axios.post('/query_investment_review_plan_list', payload);
}

export function getDetail(payload = {}) {
    return axios.post('/get_investment_review_plan_detail', payload);
}

export function saveBundle(payload = {}) {
    return axios.post('/save_investment_review_plan_bundle', payload);
}

export function saveModification(payload = {}) {
    return axios.post('/save_investment_review_modification', payload);
}

export function saveExecution(payload = {}) {
    return axios.post('/save_investment_review_execution', payload);
}

export function saveReview(payload = {}) {
    return axios.post('/save_investment_review_review', payload);
}

export function deleteModification(payload = {}) {
    return axios.post('/delete_investment_review_modification', payload);
}

export function deleteExecution(payload = {}) {
    return axios.post('/delete_investment_review_execution', payload);
}

export default {
    queryList,
    getDetail,
    saveBundle,
    saveModification,
    saveExecution,
    saveReview,
    deleteModification,
    deleteExecution,
};
