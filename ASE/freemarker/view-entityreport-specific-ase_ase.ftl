<input style="opacity:0;width:1px;height:1px;overflow:hidden;" id="top"></input>
<div class="modal-header">
	<button type="button" class="close entity-report-close" data-dismiss="modal" aria-hidden="true">&times;</button>
	<h4 class="modal-title" id="modal-title">ASE variant: ${entity.getString("snp_id")}</h4>
</div>
<#noparse>
<script>
	$(document).ready(function(){
	    $(".geneRow").click(function(e){
	        $('#'+$(this).attr('data-ensg')+'_fig').toggle();
	    });
		
		$(".geneUrl").click(function(e){
	        e.stopPropagation();
	    });
	    
	    setTimeout(function () {
	        $("#top").css("display", "none");
	    }, 500);
	});
</script>
</#noparse>

<div class="modal-body">
	
    <div class="row-fluid">
		<div class = "col-md-12">
  			<#-- ASE TABLE -->
			<table class="table table-condensed table-striped table-responsive">
				<thead></thead>
					<tbody>
						<tr>
							<th>Chromosome</th>
							<td>${entity.get("Chr")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Likelihood ratio</th>
							<td>${entity.get("Likelihood_ratio")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Binomial test P-value</th>
							<td><#if entity.get("binom_Pval") == 0>&le; 2E-311<#else>${entity.get("binom_Pval")?string("0.##E0")}</#if></td>
							
						</tr>
						
						<tr>
						
							<th>Position</th>
							<td>${entity.get("Pos")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Likelihood ratio P-value</th>
							<td>${entity.get("Likelihood_ratio_test_Pval")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Bonferroni corrected binomial test P-value</th>
							<td><#if entity.get("binom_bonferroni") == 0>&le; 2E-311<#else>${entity.get("binom_bonferroni")?string("0.##E0")}</#if></td>
							
						</tr>
						
						<tr>
						
							<th>Reference allele</th>
							<td>${entity.get("Reference_allele")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Likelihood ratio FDR</th>
							<td>${entity.get("Likelihood_ratio_test_FDR")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Binomial test FDR</th>
							<td><#if entity.get("binom_FDR") == 0>&le; 2E-311<#else>${entity.get("binom_FDR")?string("0.##E0")}</#if></td>
														
						</tr>
						
						<tr>
						
							<th>Alternative allele</th>
							<td>${entity.get("Alternative_allele")}</td>
							
							<th> </th>
							<td> </td>
							
							<th>Likelihood ratio bonferroni corrected</th>
							<td>${entity.get("Likelihood_ratio_test_bonferroni")}</td>
						
						</tr>
						
						<tr>
						
							<th>Fraction alternative allele</th>
							<td>${entity.get("Fraction_alternative_allele")}</td>
							
							<th></th>
							<td></td>
							
						</tr>
						
						<tr>
						
							<th>SNP ID</th>
							<td>
							<#if entity.getString("snp_id")?starts_with("rs")>
								<a target="_blank" href="http://identifiers.org/dbsnp/${entity.get("snp_id")}">${entity.get("snp_id")}</a>
							<#else>
								${entity.getString("snp_id")}
							</#if>
							</td>
							
							<th></th>
							<td></td>
							
						</tr>
						
						<tr>
							
							<th>Number of samples</th>
							<td>${entity.get("Samples")}</td>
							
							<th></th>
							<td></td>
							
						</tr>
						
					</tbody>
			</table>
			
		</div>
	</div>

    <#if entity!='' && entity.get("Ensembl_ID")??>
        <#assign genes=entity.get('Ensembl_ID')>
    
        <div class="row-fluid">
            <div class="col-md-12 table-responsive">
                <#-- GENE TABLE -->
                <#list genes as gene>
                    <table class="table table-condensed table-striped">                       
                        <thead>
                            <th>Gene symbol</th>
                            <th>Ensembl ID</th>
                            <th>Biotype</th>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    ${gene.Gene_symbol}
                                </td>
                                <td>
                                    <a target="_blank" href="http://identifiers.org/ensembl/${gene.Ensembl_ID}" class="geneUrl">${gene.Ensembl_ID}</a>
                                </td>
                                <td>
                                    ${gene.Biotype}
                                </td>
                            </tr>
                        </tbody> 
                    </table>
                </#list>
            </div>
        </div>

    </#if>
    
    	<#assign snp_id = entity.get("snp_id")>
	<#if snp_id?contains(":")>
		<#assign snp_id = snp_id?replace(":", "_")>
	</#if>	
	
	<#if snp_id?contains("rs")>
		<#assign chr = entity.get("Chr")>
		<#assign pos = entity.get("Pos")>
		<#assign snp_id = "${chr}_${pos}">
	</#if>
	
	<#assign chr = entity.get("Chr")>

    <div class="row-fluid">
		<div class="col-md-12" style="text-align:center;">	
			<img src="https://molgenis26.target.rug.nl/downloads/BIOS_ASE/ASEbrowserplots/chr${chr}/png/${snp_id}.png" alt="${snp_id}" width="800" height="600">
		</div>
	</div>
    
    <div class="row-fluid">
		<div class="col-md-12" style="text-align:center;">		
		
			<hr>
			<#-- Download buttons -->
			<a type="button" target="_blank" class="btn btn-primary" href="https://molgenis26.target.rug.nl/downloads/BIOS_ASE/ASEbrowserplots/chr${chr}/png/${snp_id}.png">Download ASE plot</a>
	  		</hr>
  		</div>
	</div>	
    
    
    <div class="row-fluid">
		<div class="col-md-12">		
	  		<#-- Genomebrowser here -->
			<div id="modalGenomeBrowser"></div>
		</div>
	</div>
    
    
</div>




<#-- modal footer -->
<div class="modal-footer">
	<button type="button" class="btn btn-default entity-report-close" data-dismiss="modal">close</button>
</div>

<script>
	molgenis.dataexplorer.data.createGenomeBrowser({
		pageName: 'modalGenomeBrowser', 
		noPersist: true, chr: "chr"+${entity.get("Chr")}, 
		viewStart: ${entity.get("Pos")} - 10000, 
		viewEnd: ${entity.get("Pos")} + 10000,
		disableDefaultFeaturePopup: true
	});
	
	$('.entity-report-close').on('click', function(){
	    $('#genomebrowser').css('display', 'none');
	});
	
	$("#modalGenomeBrowser").on("focusin", function(){
	    setTimeout(function() { 
	        $("#top").focus();
	    }, 10);
	    $("#top").focus();
    });
</script>


