<script>
    import { page } from '@inertiajs/inertia-svelte'
</script>


> {$page.props.page_name}

<ul>
{#each $page.props.events as event}
    <li><a href="/about/{event}">{event}</a></li>
{/each}
</ul>