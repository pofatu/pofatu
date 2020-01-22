<div>
    <dl>
        % for attr in ['technique', 'instrument', 'laboratory', 'analyst', 'date', 'reference_sample', 'comment']:
            % if getattr(ctx.method, attr):
                <dt>${attr.replace('_', ' ')}</dt>
                <dd>${getattr(ctx.method, attr)}</dd>
            % endif
        % endfor
    </dl>
</div>