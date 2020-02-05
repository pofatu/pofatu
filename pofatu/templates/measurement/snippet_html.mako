<div>
    <dl class="dl-horizontal">
        % for attr in ['instrument', 'date', 'reference_sample', 'number_of_replicates', 'detection_limit', 'total_procedural_blank_value', 'comment']:
            % if getattr(ctx.method, attr):
                <dt>${attr.replace('_', ' ')}</dt>
                <dd>${getattr(ctx.method, attr)}</dd>
            % endif
        % endfor
        % if ctx.method.references:
            <dt>reference samples</dt>
            <dd>
                <ul class="unstyled">
                    % for ref in ctx.method.references:
                        <li>
                            ${ref.as_string()}
                        </li>
                    % endfor
                </ul>
            </dd>
        % endif
    </dl>
</div>