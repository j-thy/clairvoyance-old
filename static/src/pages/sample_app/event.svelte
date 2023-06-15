<script>
    import { page } from '@inertiajs/inertia-svelte'
</script>

> {$page.props.name}

<ul>
	<li>{$page.props.servant_id}</li>
	<li>{$page.props.status}</li>
	<li>{$page.props.name}</li>
</ul>

