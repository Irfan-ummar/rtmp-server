<template>
  <div class="camera-add">
    <h2>Add New Camera</h2>
    
    <div v-if="error" class="alert error">{{ error }}</div>
    <div v-if="success" class="alert success">Camera added successfully!</div>
    
    <form @submit.prevent="addCamera" class="camera-form">
      <div class="form-group">
        <label for="name">Camera Name</label>
        <input 
          type="text" 
          id="name" 
          v-model="camera.name" 
          required
          placeholder="e.g., Front Door Camera"
        >
      </div>
      
      <div class="form-group">
        <label for="ip_address">IP Address</label>
        <input 
          type="text" 
          id="ip_address" 
          v-model="camera.ip_address" 
          required
          placeholder="e.g., 192.168.1.100"
          pattern="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        >
      </div>
      
      <div class="form-group">
        <label for="rtmp_port">RTMP Port</label>
        <input 
          type="number" 
          id="rtmp_port" 
          v-model="camera.rtmp_port" 
          required
          placeholder="e.g., 1935"
          min="1"
          max="65535"
        >
      </div>
      
      <div class="form-group">
        <label for="app_name">App Name</label>
        <input 
          type="text" 
          id="app_name" 
          v-model="camera.app_name" 
          required
          placeholder="e.g., live"
        >
      </div>

      <div class="form-group">
        <label for="stream_id">Stream ID</label>
        <input 
          type="text" 
          id="stream_id" 
          v-model="camera.stream_id" 
          required
          placeholder="e.g., stream1"
        >
      </div>
      
      <div class="form-group">
        <label class="checkbox-container">
          <input type="checkbox" v-model="camera.active">
          <span class="checkmark"></span>
          Start Stream Immediately
        </label>
      </div>
      
      <div class="form-actions">
        <button type="button" @click="goBack" class="btn btn-secondary">Cancel</button>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Adding...' : 'Add Camera' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'CameraAddView',
  
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // Form data
    const camera = reactive({
      name: '',
      ip_address: '',
      rtmp_port: 1935,
      app_name: 'live',
      stream_id: '',
      active: false
    })
    
    // State
    const success = ref(false)
    
    // Computed properties from Vuex store
    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)
    
    // Methods
    const addCamera = async () => {
      try {
        const newCamera = await store.dispatch('createCamera', camera)
        success.value = true
        
        // Redirect to camera detail view after a short delay
        setTimeout(() => {
          router.push({ path: `/cameras/${newCamera.id}` })
        }, 1500)
      } catch (error) {
        console.error('Error adding camera:', error)
      }
    }
    
    const goBack = () => {
      router.push({ path: '/' })
    }
    
    return {
      camera,
      loading,
      error,
      success,
      addCamera,
      goBack
    }
  }
}
</script>

<style scoped>
.camera-add {
  max-width: 600px;
  margin: 0 auto;
}

.alert {
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.camera-form {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-container input {
  margin-right: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 