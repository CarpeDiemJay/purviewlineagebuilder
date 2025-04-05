<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-2xl font-bold text-gray-900">Purview Lineage Builder</span>
            </div>
          </div>
          <div class="flex items-center">
            <button @click="openSettings" class="p-2 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Left Side Asset -->
            <div class="space-y-4">
              <h2 class="text-lg font-medium text-gray-900">Left Side Asset</h2>
              <div class="relative">
                <input
                  type="text"
                  v-model="leftSearch"
                  @input="searchLeftAssets"
                  placeholder="Search for SQL tables..."
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <div v-if="leftResults.length" class="absolute z-10 mt-1 w-full bg-white rounded-md shadow-lg">
                  <ul class="max-h-60 rounded-md py-1 text-base overflow-auto focus:outline-none">
                    <li
                      v-for="asset in leftResults"
                      :key="asset.qualifiedName"
                      @click="selectLeftAsset(asset)"
                      class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-gray-100"
                    >
                      <span class="block truncate">{{ asset.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div v-if="selectedLeftAsset" class="p-4 bg-gray-50 rounded-md">
                <h3 class="text-sm font-medium text-gray-900">Selected Asset</h3>
                <p class="mt-1 text-sm text-gray-500">{{ selectedLeftAsset.name }}</p>
              </div>
            </div>

            <!-- Right Side Asset -->
            <div class="space-y-4">
              <h2 class="text-lg font-medium text-gray-900">Right Side Asset</h2>
              <div class="relative">
                <input
                  type="text"
                  v-model="rightSearch"
                  @input="searchRightAssets"
                  placeholder="Search for Power BI datasets..."
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <div v-if="rightResults.length" class="absolute z-10 mt-1 w-full bg-white rounded-md shadow-lg">
                  <ul class="max-h-60 rounded-md py-1 text-base overflow-auto focus:outline-none">
                    <li
                      v-for="asset in rightResults"
                      :key="asset.qualifiedName"
                      @click="selectRightAsset(asset)"
                      class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-gray-100"
                    >
                      <span class="block truncate">{{ asset.name }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div v-if="selectedRightAsset" class="p-4 bg-gray-50 rounded-md">
                <h3 class="text-sm font-medium text-gray-900">Selected Asset</h3>
                <p class="mt-1 text-sm text-gray-500">{{ selectedRightAsset.name }}</p>
              </div>
            </div>
          </div>

          <div class="mt-6">
            <button
              @click="createLineage"
              :disabled="!canCreateLineage"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Create Lineage
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Settings Modal -->
    <div v-if="showSettings" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Settings</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Account Name</label>
                <input type="text" v-model="settings.accountName" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Client ID</label>
                <input type="text" v-model="settings.clientId" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Tenant ID</label>
                <input type="text" v-model="settings.tenantId" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="saveSettings" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm">
              Save
            </button>
            <button @click="closeSettings" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const leftSearch = ref('')
const rightSearch = ref('')
const leftResults = ref([])
const rightResults = ref([])
const selectedLeftAsset = ref(null)
const selectedRightAsset = ref(null)
const showSettings = ref(false)
const settings = ref({
  accountName: '',
  clientId: '',
  tenantId: ''
})

const canCreateLineage = computed(() => {
  return selectedLeftAsset.value && selectedRightAsset.value
})

const searchLeftAssets = async () => {
  if (leftSearch.value.length < 2) {
    leftResults.value = []
    return
  }
  try {
    const response = await axios.get(`/api/search?type=sql&query=${leftSearch.value}`)
    leftResults.value = response.data
  } catch (error) {
    console.error('Error searching left assets:', error)
  }
}

const searchRightAssets = async () => {
  if (rightSearch.value.length < 2) {
    rightResults.value = []
    return
  }
  try {
    const response = await axios.get(`/api/search?type=powerbi&query=${rightSearch.value}`)
    rightResults.value = response.data
  } catch (error) {
    console.error('Error searching right assets:', error)
  }
}

const selectLeftAsset = (asset) => {
  selectedLeftAsset.value = asset
  leftResults.value = []
}

const selectRightAsset = (asset) => {
  selectedRightAsset.value = asset
  rightResults.value = []
}

const createLineage = async () => {
  if (!canCreateLineage.value) return
  
  try {
    await axios.post('/api/lineage', {
      leftAsset: selectedLeftAsset.value,
      rightAsset: selectedRightAsset.value
    })
    // Show success message
    alert('Lineage created successfully!')
  } catch (error) {
    console.error('Error creating lineage:', error)
    alert('Failed to create lineage. Please try again.')
  }
}

const openSettings = () => {
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const saveSettings = async () => {
  try {
    await axios.post('/api/settings', settings.value)
    showSettings.value = false
    alert('Settings saved successfully!')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Failed to save settings. Please try again.')
  }
}
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
</style> 