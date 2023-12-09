<template>
  <div>
    <div class="flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
      <div class="flex-1"></div>
      <h1 class="text-4xl font-bold flex-shrink" @click="redirectToManagement">Welcome, {{ username }}, {{isAdmin}}!</h1>
      <div class="flex-1 flex justify-end">
        <DarkModeSwitch class="non-printing"></DarkModeSwitch>
      </div>
    </div>

    <div class="box-content h-1/4 w-1/2 p-4 border border-gray-300 ml-8 rounded-lg">
      <div class="text-2xl pl-2 font-bold mb-4">Client Lookup</div>
      <div class="pl-2 mb-4 whitespace-pre-line">On this page, enter your client name in the search box below. Then, click your client name to view all of the policies that are available under your company name.</div>
      <input v-model="textInput" type="text" placeholder="Enter client name:" class="w-1/2 ml-2 px-2 py-2 border border-gray-300 dark:bg-gray-800 dark:border-gray-500 rounded-md shadow-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
    </div>

    <div class="grid grid-cols-4 gap-2 mt-4 px-8 pb-5">
        <!-- Add Button -->
        <button v-if="isAdmin" @click="openModal" class="cell-button px-2 py-1 border rounded-md hover:bg-gray-200 dark:border-gray-500 dark:hover:bg-gray-500 cursor-pointer">
            <div class="circle-icon border-black dark:border-gray-200">
                <span class="plus-icon dark:text-gray-200">+</span>
            </div>
        </button>

        <!-- Business Items -->
        <div 
            v-for="business in sortedAndFilteredBusinesses" 
            :key="business.business_id"
            :ref="el => setBusinessCellRef(el, business)"
            :class="['group', 'business-cell', 'px-2', 'py-1', 'border', 'rounded-md', 'hover:bg-gray-200', 'dark:hover:bg-gray-500', 'dark:hover:text-gray-200', 'cursor-pointer', 'relative', { 'highlight-business': highlightBusinessId === business.business_id }]"
            @click.stop="redirectToBusinessInfo(business)">
            {{ business.business_name }}
            <span class="absolute top-0 right-0 p-1 hidden group-hover:block">
                <TrashIcon class="h-6 w-6" @click.stop="deleteBusiness(business)"/>
            </span>
        </div>
    </div>


    <TransitionRoot :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full md:w-[800px] transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all z-40">
              <BusinessForm></BusinessForm>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot :show="isDeleteModalOpen" as="template">
      <Dialog as="div" class="fixed inset-0 z-10 overflow-y-auto" @close="closeDeleteModal">
        <div class="flex min-h-screen items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="ease-in duration-200"
            leave-from="opacity-100"
            leave-to="opacity-0"
          >
            <div class="fixed inset-0 bg-black opacity-30" aria-hidden="true"></div>
          </TransitionChild>

          <!-- Modal Panel -->
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
              <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                Confirm Deletion
              </DialogTitle>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Are you sure you want to delete this business? This action cannot be undone.
                </p>
              </div>

              <div class="mt-4 flex justify-end gap-3">
                <button type="button" class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2" @click="closeDeleteModal">
                  Cancel
                </button>
                <button type="button" class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2" @click="confirmDelete">
                  Delete
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
  <div>
    <button @click="logOut">Log out</button>
  </div>
</template>

<script>
import { checkAdminStatus } from '@/adminCheck';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { TrashIcon } from '@heroicons/vue/24/outline';
import axios from 'axios';
import Cookies from 'js-cookie';
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import api from '../api.js';
import EventBus from '../eventBus';
import BusinessForm from './BusinessForm.vue';
import DarkModeSwitch from './DarkModeSwitch.vue';

export default {
    name: 'PostingPage',
    components: {
        DarkModeSwitch,
        TransitionRoot,
        TransitionChild,
        Dialog,
        DialogPanel,
        DialogTitle,
        BusinessForm,
        TrashIcon
    },
    setup() {
        const store = useStore();
        const router = useRouter();
        const userId = computed(() => store.getters['accounts/getUserId']);
        const username = computed(() => store.getters['accounts/getUsername']);
        const textInput = ref('');
        const businesses = ref([]);
        const isAdmin = ref(false);
        const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedDarkMode = window.localStorage.getItem('isDarkMode');
        const initialDarkMode = savedDarkMode !== null ? savedDarkMode === 'true' : prefersDarkMode;
        const isDarkMode = ref(initialDarkMode);
        const isOpen = ref(false);
        const highlightBusinessId = ref(null);
        const businessCellRefs = ref({});
        const isDeleteModalOpen = ref(false);
        const businessToDelete = ref(null);

        const redirectToManagement = () => {
            router.push({
                name: 'ManageAccount'
            });
        };

        const fetchCurrentUser = () => {
            const csrf_access = store.state.accounts.access_csrf;
            if (!csrf_access) {
                fetchUserFromGoogleSession();
                return;
            }
            api.get('/protected', {
                headers: {
                    'X-CSRF-TOKEN': csrf_access
                },
                withCredentials: true
            })
                .then(response => {
                const { data } = response;
                store.dispatch('accounts/setUserCredentials', {
                    id: data.id,
                    username: data.logged_in_as,
                });
                console.log("Updated store state with JWT user data:", store.state.accounts);
            })
                .catch(error => {
                console.error('Error fetching current user:', error);
            });
        };

        const fetchUserFromGoogleSession = () => {
            console.log("Fetching Google session user...");
            api.get('/google_user_data', {
                withCredentials: true
            })
                .then(response => {
                const { data } = response;
                const loggedIn = Cookies.get('logged_in');
                store.dispatch('accounts/setUserCredentials', {
                    id: data.account_id,
                    username: data.account_name,
                    isAuthenticated: true
                });
                Cookies.remove(loggedIn);
                console.log("Updated store state with Google user data:", store.state.accounts);
            })
                .catch(error => {
                console.error('Error fetching Google session user:', error);
            });
        };
        const logOut = () => {
            axios.post('https://localhost:5000/logout', {}, { withCredentials: true })
                .then(response => {
                console.log(response.data.message);
                store.dispatch('accounts/logOut');
                router.push('/');
            })
                .catch(error => {
                console.error('Logout failed:', error);
            });
        };

        const setBusinessCellRef = (el, business) => {
          if (el && business) {
            businessCellRefs.value[business.business_id] = el;
          }
        };

        const deleteBusiness = (business) => {
          console.log("Deleting business with ID:", business.business_id);
          businessToDelete.value = business;
          isDeleteModalOpen.value = true;
        };

        const closeDeleteModal = () => {
          isDeleteModalOpen.value = false;
          businessToDelete.value = null;
        };

        const confirmDelete = async () => {
          if (businessToDelete.value) {
            await axios.delete(`https://localhost:5000/delete_business/${businessToDelete.value.business_id}`)
              .then(response => {
                console.log("Deleted successfully", response);
                businesses.value = businesses.value.filter(b => b.business_id !== businessToDelete.value.business_id);
              })
              .catch(error => {
                console.error("Error deleting client", error);
              });
          }
          closeDeleteModal();
      };


        onMounted(async () => {
            try {
                EventBus.on('business-added', handleBusinessAdded);
                EventBus.on('close-modal', () => {
                    console.log("EventBus 'close-modal' event received");
                    closeModal();
                });
                fetchCurrentUser();
                isAdmin.value = await checkAdminStatus();
                console.log("Admin deez nuts", isAdmin.value);
                const response = await axios.get('https://localhost:5000/api/businesses');
                businesses.value = response.data;
            } catch (error) {
                console.error(error);
            }
        });

        onUnmounted(() => {
          EventBus.off('close-modal', closeModal);
          EventBus.off('business-added', handleBusinessAdded);
        });

        const sortedAndFilteredBusinesses = computed(() => {
          if (!businesses.value) return [];

          let filteredBusinesses = businesses.value.filter(b => b != null);
          let val = textInput.value.toUpperCase();
          return filteredBusinesses
            .filter(business => business.business_name.toUpperCase().includes(val))
            .sort((a, b) => a.business_name.localeCompare(b.business_name));
        });

        const redirectToBusinessInfo = (business) => {
            router.push({
                name: 'BusinessInfo',
                query: {
                    businessName: business.business_name
                }
            });
        };

        const handleBusinessAdded = (business) => {
          console.log('New business added:', business);
          businesses.value.push(business);
          highlightBusinessId.value = business.business_id;

          // Remove highlight after a delay
          setTimeout(() => {
            highlightBusinessId.value = null;
          }, 4000);
          nextTick(() => {
            const businessCell = businessCellRefs.value[business.business_id];
            if (businessCell) {
              businessCell.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          });
        };


        const openModal = () => {
            isOpen.value = true;
        };

        const closeModal = () => {
            isOpen.value = false;
        };

        return {
            userId,
            username,
            api,
            redirectToManagement,
            logOut,
            fetchCurrentUser,
            fetchUserFromGoogleSession,
            textInput,
            businesses,
            isDarkMode,
            sortedAndFilteredBusinesses,
            redirectToBusinessInfo,
            checkAdminStatus,
            isAdmin,
            isOpen,
            openModal,
            closeModal,
            EventBus,
            handleBusinessAdded,
            highlightBusinessId,
            businessCellRefs,
            setBusinessCellRef,
            deleteBusiness,
            isDeleteModalOpen,
            confirmDelete,
            closeDeleteModal
        };
    }
};
</script>

<style scoped>
.cell-button {
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border: 2px dashed #000; /* Standard border color */
  border-radius: 50%;
  background-color: transparent;
}

.plus-icon {
  font-size: 24px;
  color: #000;
}

/* Modal Background */
.dialog-background {
  position: fixed; /* Fix the position */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto; /* Enable scrolling inside the modal */
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
}

/* Modal Content */
.dialog-content {
  position: relative;
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin: 10% auto;
  max-width: 500px;
}

.highlight-business {
  animation: pulsate 2s infinite;
}

@keyframes pulsate {
  0%, 100% {
    background-color: transparent;
  }
  50% {
    background-color: rgba(255, 255, 0, 0.2);
  }
}
</style>
