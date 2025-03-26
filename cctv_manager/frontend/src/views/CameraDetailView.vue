<template>
  <div class="camera-detail">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!camera" class="not-found">Camera not found</div>
    <div v-else>
      <div class="camera-header">
        <h2>{{ camera.name }}</h2>
        <div class="camera-status">
          <span :class="['status-badge', camera.active ? 'active' : 'inactive']">
            {{ camera.active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>
      
      <div class="camera-info">
        <div class="info-group">
          <h3>Camera Details</h3>
          <p><strong>IP Address:</strong> {{ camera.ip_address }}</p>
          <p><strong>RTSP Port:</strong> {{ camera.rtsp_port }}</p>
          <p><strong>Stream Path:</strong> {{ camera.stream_path }}</p>
          <p><strong>RTSP URL:</strong> {{ camera.rtsp_url }}</p>
          <p><strong>RTMP URL:</strong> {{ camera.rtmp_url }}</p>
        </div>
        
        <div class="control-group">
          <h3>Stream Controls</h3>
          <div class="button-group">
            <button 
              v-if="!camera.active" 
              @click="startStream" 
              class="btn btn-start"
              :disabled="actionLoading"
            >
              Start Stream
            </button>
            <button 
              v-else 
              @click="stopStream" 
              class="btn btn-stop"
              :disabled="actionLoading"
            >
              Stop Stream
            </button>
            <button 
              @click="refreshCamera" 
              class="btn btn-refresh"
              :disabled="actionLoading"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>
      
      <div class="stream-container">
        <h3>Live Stream</h3>
        <div v-if="!camera.active" class="stream-inactive">
          <p>Stream is currently inactive. Start the stream to view video.</p>
        </div>
        <div v-else-if="!camera.hls_url" class="stream-loading">
          <p>Stream is starting. Please wait...</p>
        </div>
        <div v-else class="video-container">
          <video ref="videoPlayer" controls autoplay muted></video>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import Hls from 'hls.js'

export default {
  name: 'CameraDetailView',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  
  setup(props) {
    const store = useStore()
    
    const videoPlayer = ref(null)
    const hls = ref(null)
    const actionLoading = ref(false)
    
    // Computed properties from Vuex store
    const camera = computed(() => store.state.currentCamera)
    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)
    
    // Fetch camera data
    const fetchCameraData = async () => {
      try {
        await store.dispatch('fetchCamera', props.id)
      } catch (error) {
        console.error('Error fetching camera:', error)
      }
    }
    
    // Initialize HLS.js player
    const initializePlayer = () => {
      if (!camera.value || !camera.value.hls_url || !videoPlayer.value) return
      
      // Destroy existing HLS instance if it exists
      if (hls.value) {
        hls.value.destroy()
        hls.value = null
      }
      
      // Check if browser supports HLS natively (Safari)
      if (videoPlayer.value.canPlayType('application/vnd.apple.mpegurl')) {
        videoPlayer.value.src = camera.value.hls_url
        videoPlayer.value.addEventListener('loadedmetadata', () => {
          videoPlayer.value.play()
        })
      } 
      // Otherwise use HLS.js
      else if (Hls.isSupported()) {
        hls.value = new Hls()
        hls.value.loadSource(camera.value.hls_url)
        hls.value.attachMedia(videoPlayer.value)
        hls.value.on(Hls.Events.MANIFEST_PARSED, () => {
          videoPlayer.value.play()
        })
        
        // Error handling
        hls.value.on(Hls.Events.ERROR, (event, data) => {
          if (data.fatal) {
            switch(data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                console.error('HLS network error', data)
                // Try to recover network error
                hls.value.startLoad()
                break
              case Hls.ErrorTypes.MEDIA_ERROR:
                console.error('HLS media error', data)
                // Try to recover media error
                hls.value.recoverMediaError()
                break
              default:
                // Cannot recover from other errors
                console.error('Fatal HLS error', data)
                break
            }
          }
        })
      } else {
        console.error('HLS is not supported in this browser')
      }
    }
    
    // Stream control methods
    const startStream = async () => {
      if (!camera.value) return;
      
      actionLoading.value = true
      try {
        await store.dispatch('startStream', props.id)
        await fetchCameraData()
      } catch (error) {
        console.error('Error starting stream:', error)
      } finally {
        actionLoading.value = false
      }
    }
    
    const stopStream = async () => {
      if (!camera.value) return;
      
      actionLoading.value = true
      try {
        await store.dispatch('stopStream', props.id)
        await fetchCameraData()
      } catch (error) {
        console.error('Error stopping stream:', error)
      } finally {
        actionLoading.value = false
      }
    }
    
    const refreshCamera = async () => {
      actionLoading.value = true
      try {
        await fetchCameraData()
      } catch (error) {
        console.error('Error refreshing camera:', error)
      } finally {
        actionLoading.value = false
      }
    }
    
    // Lifecycle hooks
    onMounted(() => {
      fetchCameraData()
    })
    
    // Watch for changes in camera or HLS URL to initialize player
    watch(
      () => camera.value?.hls_url,
      (newValue) => {
        if (newValue) {
          initializePlayer()
        }
      }
    )
    
    // Clean up HLS instance before component is unmounted
    onBeforeUnmount(() => {
      if (hls.value) {
        hls.value.destroy()
        hls.value = null
      }
    })
    
    return {
      camera,
      loading,
      error,
      videoPlayer,
      actionLoading,
      startStream,
      stopStream,
      refreshCamera
    }
  }
}
</script>

<style scoped>
.camera-detail {
  padding: 1rem;
}

.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.camera-header h2 {
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  font-weight: bold;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.camera-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-group, .control-group {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info-group h3, .control-group h3 {
  margin-top: 0;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.button-group {
  display: flex;
  gap: 0.75rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.btn-start {
  background-color: #d4edda;
  color: #155724;
}

.btn-stop {
  background-color: #f8d7da;
  color: #721c24;
}

.btn-refresh {
  background-color: #e2f3fc;
  color: #0c5460;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.stream-container {
  background-color: #1a1a1a;
  color: white;
  padding: 1rem;
  border-radius: 4px;
}

.stream-container h3 {
  margin-top: 0;
}

.video-container {
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  position: relative;
}

.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black;
}

.stream-inactive, .stream-loading {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #333;
  text-align: center;
  border-radius: 4px;
}

.loading, .error, .not-found {
  text-align: center;
  margin-top: 2rem;
}

.error {
  color: #721c24;
}

@media (max-width: 768px) {
  .camera-info {
    grid-template-columns: 1fr;
  }
}
</style> 