<template>
  <div class="dashboard">
    <h2>Camera Dashboard</h2>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!filteredCameras || filteredCameras.length === 0" class="empty-state">
      <p>No cameras added yet.</p>
      <router-link to="/cameras/add" class="btn btn-primary">Add Camera</router-link>
    </div>
    <div v-else class="camera-grid">
      <div v-for="camera in filteredCameras" :key="camera.id" class="camera-card">
        <div class="camera-header">
          <h3>{{ camera.name }}</h3>
          <span :class="['status-badge', camera.active ? 'active' : 'inactive']">
            {{ camera.active ? 'Active' : 'Inactive' }}
          </span>
        </div>
        <div class="camera-details">
          <p><strong>IP:</strong> {{ camera.ip_address }}</p>
          <p><strong>RTSP URL:</strong> {{ camera.rtsp_url }}</p>
        </div>
        <div class="camera-actions">
          <router-link :to="`/cameras/${camera.id}`" class="btn btn-view">View</router-link>
          <button 
            v-if="!camera.active" 
            @click="startStream(camera.id)" 
            class="btn btn-start"
            :disabled="actionLoading"
          >
            Start Stream
          </button>
          <button 
            v-else 
            @click="stopStream(camera.id)" 
            class="btn btn-stop"
            :disabled="actionLoading"
          >
            Stop Stream
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'DashboardView',
  
  setup() {
    const store = useStore()
    const actionLoading = ref(false)
    
    // Computed properties from Vuex store
    const cameras = computed(() => store.state.cameras || [])
    
    // Filter out null cameras into a separate computed property
    const filteredCameras = computed(() => {
      return cameras.value.filter(camera => camera != null);
    })
    
    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)
    
    // Fetch cameras on component mount
    onMounted(() => {
      store.dispatch('fetchCameras')
    })
    
    // Methods
    const startStream = async (cameraId) => {
      actionLoading.value = true
      try {
        await store.dispatch('startStream', cameraId)
        await store.dispatch('fetchCameras')
      } catch (error) {
        console.error('Error starting stream:', error)
      } finally {
        actionLoading.value = false
      }
    }
    
    const stopStream = async (cameraId) => {
      actionLoading.value = true
      try {
        await store.dispatch('stopStream', cameraId)
        await store.dispatch('fetchCameras')
      } catch (error) {
        console.error('Error stopping stream:', error)
      } finally {
        actionLoading.value = false
      }
    }
    
    return {
      cameras,
      filteredCameras,
      loading,
      error,
      actionLoading,
      startStream,
      stopStream
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 1rem;
}

.camera-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.camera-card {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.camera-header h3 {
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.camera-details {
  margin-bottom: 1rem;
}

.camera-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.camera-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
}

.btn-view {
  background-color: #e2f3fc;
  color: #0c5460;
}

.btn-start {
  background-color: #d4edda;
  color: #155724;
}

.btn-stop {
  background-color: #f8d7da;
  color: #721c24;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading, .error, .empty-state {
  text-align: center;
  margin-top: 2rem;
}

.error {
  color: #721c24;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  display: inline-block;
  margin-top: 1rem;
}
</style> 