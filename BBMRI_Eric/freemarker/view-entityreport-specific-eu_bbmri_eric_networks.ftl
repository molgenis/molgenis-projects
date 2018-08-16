<div class="modal-content">
	<div class="modal-header">
		<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
		<h2 class="modal-title">${entity.get('name')}</h2>
		<#if entity.get('acronym')??>
			<small><strong>Acronym</strong>: ${entity.get('acronym')}</small>
		</#if>
	</div>    

	<div class="modal-body">
		<div class="row">
			<div class="col-md-12">
				<div class="media-body">
					<p class="lead"><h4>${entity.get('description')}</h4></p>
				</div>
			</div>
		</div>
        <div class="row">
        	<div class="col-md-6">
        		<table class="table table-striped">
        			<tr>
        				<th>Common collection focus</th>
        				<td>${entity.get('common_collection_focus')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common charter</th>
        				<td>${entity.get('common_charter')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common sops</th>
        				<td>${entity.get('common_sops')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common data access policy</th>
        				<td>${entity.get('common_data_access_policy')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common sample access policy</th>
        				<td>${entity.get('common_sample_access_policy')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common mta</th>
        				<td>${entity.get('common_mta')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common image access policy</th>
        				<td>${entity.get('common_image_access_policy')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common image mta</th>
        				<td>${entity.get('common_image_mta')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common representation</th>
        				<td>${entity.get('common_representation')?string("yes", "no")}</td>
        			</tr>
        			<tr>
        				<th>Common url</th>
        				<td>${entity.get('common_url')?string("yes", "no")}</td>
        			</tr>
        		</table>
			</div>
			<div class="col-md-6">
        		<table class="table table-striped">
        			<tr>
        				<th>URL</th>
        				<td>${entity.get('url')}</td>
        			</tr>
        			<#if entity.get('juridical_person')??>
						<tr>
							<th>Juridical person</th>
							<td>${entity.get('juridical_person')}</td>
						</tr>
					</#if>
					<#if entity.get('contact')??>
        			<tr>
        				<th>Contact</th>
        				<td>${entity.get('contact').email}</td>
        			</tr>
        			<tr>
        				<th>Contact priority</th>
        				<td>${entity.get('contact_priority')}</td>
        			</tr>
        			</#if>
        			<#if entity.get('latitude')??>
						<tr>
							<th>Latitude</th>
							<td>${entity.get('latitude')}</td>
						</tr>
					</#if>
					<#if entity.get('longitude')??>
						<tr>
							<th>Longitude</th>
							<td>${entity.get('longitude')}</td>
						</tr>
					</#if>
					<#if entity.get('parent_network')?has_content>
						<tr>
							<th>Parent network</th>
							<td>${entity.get('parent_network')}</td>
						</tr>
					</#if>
        		</table>
			</div>
        </div>
        <div class="row">
    		<div class="col-md-12">
    			<h3 id="collection-title" style="display:none">Collections</h3>
    			<p id="collections"></p>
    		</div>
    	</div>
	</div>
	
	<div class="modal-footer">
		<button type="button" class="btn btn-default" data-dismiss="modal">close</button>
	</div>
</div>
<script>
	var id = "${entity.id}"
	$.get("/api/v2/eu_bbmri_eric_collections?q=network=="+id).done(function(data){
		var collections = $.map(data.items, function(obj){
			$('#collection-title').show()
			$('#collections').append(obj.name+"<br/>")
			return obj.name
		})
	})
</script>