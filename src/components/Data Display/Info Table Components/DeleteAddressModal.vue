<template>
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
                  Are you sure you want to delete this address? This action cannot be undone.
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
</template>

<script>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { inject } from 'vue';

export default {
  components: {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionRoot,
    TransitionChild
  },
  setup() {
    const isDeleteModalOpen = inject('isDeleteModalOpen');
    const addressToDelete = inject('addressToDelete');
    const addressIds = inject('addressIds');
    const fetchBusinessData = inject('fetchBusinessData');
    const openDeleteModal = inject('openDeleteModal');
    const closeDeleteModal = inject('closeDeleteModal');
    const confirmDelete = inject('confirmDelete');

    return {
      addressToDelete,
      addressIds,
      openDeleteModal,
      closeDeleteModal,
      confirmDelete,
      isDeleteModalOpen,
      fetchBusinessData
    };
  }
};
</script>
