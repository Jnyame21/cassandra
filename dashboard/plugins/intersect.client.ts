import type { DirectiveBinding } from 'vue';

// Create the directive
export default defineNuxtPlugin((nuxtApp) => {
  // Register the directive
  nuxtApp.vueApp.directive('intersect', {
    // Called when the directive is bound to the element
    mounted(el: HTMLElement, binding: DirectiveBinding) {
      const options = {
        root: null, // The viewport by default
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
      };

      // The callback for when the intersection occurs
      const callback = (entries: IntersectionObserverEntry[]) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Call the provided method with `true` when the element is visible
            binding.value(true);
          } else {
            // Call the provided method with `false` when the element is not visible
            binding.value(false);
          }
        });
      };

      // Create a new IntersectionObserver instance
      const observer = new IntersectionObserver(callback, options);

      // Start observing the element
      observer.observe(el);

      // Save the observer instance for cleanup
      (el as any)._observer = observer;
    },

    // Called when the directive is unbound from the element
    unmounted(el: HTMLElement) {
      // Clean up the observer when the element is removed from the DOM
      if ((el as any)._observer) {
        (el as any)._observer.disconnect();
        delete (el as any)._observer; // Clean up the reference
      }
    }
  });
});

