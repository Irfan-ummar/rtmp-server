<template>
  <div class="app">
    <header class="app-header">
      <h1>CCTV Camera Manager</h1>
      <nav>
        <router-link to="/">Dashboard</router-link> |
        <router-link to="/cameras/add">Add Camera</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.app-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
}

.app-header h1 {
  margin-top: 0;
  color: #333;
}

nav {
  margin-top: 1rem;
}

nav a {
  color: #2c3e50;
  text-decoration: none;
  margin-right: 1rem;
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}

main {
  background-color: white;
  padding: 1rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style> 