import { createStore } from 'vuex'
import cameraService from '../services/cameraService'

export default createStore({
  state: {
    cameras: [],
    currentCamera: null,
    loading: false,
    error: null
  },
  getters: {
    getCameraById: (state) => (id) => {
      return state.cameras.find(camera => camera && camera.id === parseInt(id))
    }
  },
  mutations: {
    SET_CAMERAS(state, cameras) {
      state.cameras = cameras || []
    },
    SET_CURRENT_CAMERA(state, camera) {
      state.currentCamera = camera
    },
    ADD_CAMERA(state, camera) {
      if (!Array.isArray(state.cameras)) {
        state.cameras = []
      }
      if (camera) {
        state.cameras.push(camera)
      }
    },
    UPDATE_CAMERA(state, updatedCamera) {
      if (!updatedCamera) return
      
      if (!Array.isArray(state.cameras)) {
        state.cameras = []
        return
      }
      
      const index = state.cameras.findIndex(c => c && c.id === updatedCamera.id)
      if (index !== -1) {
        state.cameras.splice(index, 1, updatedCamera)
      }
    },
    DELETE_CAMERA(state, cameraId) {
      if (!Array.isArray(state.cameras)) {
        state.cameras = []
        return
      }
      state.cameras = state.cameras.filter(c => c && c.id !== cameraId)
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  actions: {
    async fetchCameras({ commit }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.getCameras()
        if (response && response.data && Array.isArray(response.data)) {
          commit('SET_CAMERAS', response.data)
        } else {
          commit('SET_CAMERAS', [])
        }
      } catch (error) {
        console.error('Error fetching cameras:', error)
        commit('SET_ERROR', error.message || 'Error fetching cameras')
        commit('SET_CAMERAS', [])
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchCamera({ commit }, cameraId) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.getCamera(cameraId)
        if (response && response.data) {
          commit('SET_CURRENT_CAMERA', response.data)
          return response.data
        }
        return null
      } catch (error) {
        console.error('Error fetching camera:', error)
        commit('SET_ERROR', error.message || 'Error fetching camera')
        commit('SET_CURRENT_CAMERA', null)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createCamera({ commit }, cameraData) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.createCamera(cameraData)
        if (response && response.data) {
          commit('ADD_CAMERA', response.data)
          return response.data
        }
        return null
      } catch (error) {
        console.error('Error creating camera:', error)
        commit('SET_ERROR', error.message || 'Error creating camera')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async updateCamera({ commit }, { id, data }) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.updateCamera(id, data)
        if (response && response.data) {
          commit('UPDATE_CAMERA', response.data)
          return response.data
        }
        return null
      } catch (error) {
        console.error('Error updating camera:', error)
        commit('SET_ERROR', error.message || 'Error updating camera')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async deleteCamera({ commit }, cameraId) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        await cameraService.deleteCamera(cameraId)
        commit('DELETE_CAMERA', cameraId)
      } catch (error) {
        console.error('Error deleting camera:', error)
        commit('SET_ERROR', error.message || 'Error deleting camera')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async startStream({ commit }, cameraId) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.startStream(cameraId)
        return response?.data || { status: 'unknown' }
      } catch (error) {
        console.error('Error starting stream:', error)
        commit('SET_ERROR', error.message || 'Error starting stream')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async stopStream({ commit }, cameraId) {
      commit('SET_LOADING', true)
      commit('CLEAR_ERROR')
      try {
        const response = await cameraService.stopStream(cameraId)
        return response?.data || { status: 'unknown' }
      } catch (error) {
        console.error('Error stopping stream:', error)
        commit('SET_ERROR', error.message || 'Error stopping stream')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
}) 