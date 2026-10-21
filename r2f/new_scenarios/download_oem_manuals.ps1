# Download public OEM manuals and open RP-1043 evidence papers
# into new_scenarios/references
# Run:  powershell -File .\download_oem_manuals.ps1

$ErrorActionPreference = "Continue"
$dest = Join-Path $PSScriptRoot "references"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$files = @(
    @{
        Name = "ASHRAE_RP-1043_evidence_MDPI_Buildings_2024.pdf"
        Url  = "https://www.mdpi.com/2075-5309/14/6/1835/pdf"
        Note = "Open paper that reprints the RP-1043 seven-fault table (not the paywalled ASHRAE store ZIP)."
    },
    @{
        Name = "ASHRAE_RP-1043_evidence_MDPI_Actuators_2023.pdf"
        Url  = "https://www.mdpi.com/2076-0825/12/6/242/pdf"
        Note = "Open paper that reprints RP-1043 SL1-SL4 percentages."
    },
    @{
        Name = "ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf"
        Url  = "https://www.jstage.jst.go.jp/article/aiue/2019/1/2019_aiue2019047/_pdf/-char/ja"
        Note = "Open paper describing the RP-1043 experiment and fault list, including faulty expansion valve."
    },
    @{
        Name = "Trane_CVHE-SVX02Q-EN.pdf"
        Url  = "https://www.trane.com/content/dam/Trane/Commercial/global/products-systems/equipment/chillers/water-cooled/centrifugal-liquid/CVHE-SVX02Q-EN_03142020.pdf"
        Note = "Trane CenTraVac IOM"
    },
    @{
        Name = "Trane_CVHE-SVX005E-EN.pdf"
        Url  = "https://elibrary.tranetechnologies.com/public/commercial-hvac/Literature/Installation%20Operation%20and%20Maintenance/CVHE-SVX005E-EN_04112026.pdf"
        Note = "Trane CenTraVac IOM (later)"
    },
    @{
        Name = "Trane_CVHE-SVU01E-EN_CH530.pdf"
        Url  = "https://surplusgroup.com/wp-content/themes/SurplusGroup/media/53168/cvhe-svu01e-en_0405.pdf"
        Note = "Trane CH530 operation"
    },
    @{
        Name = "Carrier_19XR_startup.pdf"
        Url  = "https://www.carrier.com/commercial/en/kw/media/Start%20up%20manual_tcm477-145050.pdf"
        Note = "Carrier 19XR start-up / cycle"
    },
    @{
        Name = "York_YK_Style_G_160.75.pdf"
        Url  = "https://lms.genpact.com/showcase_LMS/Learning/Chiller_JobAid/assets/resources/Model_YK_(Style_G)_R-134a.pdf"
        Note = "York / JCI YK Style G O&M"
    },
    @{
        Name = "Daikin_IOM1210_Magnitude_WMC-D.pdf"
        Url  = "https://tahoeweb.daikinapplied.com/api/general/DownloadDocumentByName/media/IOM1210-8_WMC-D_01102023_HR.pdf/"
        Note = "Daikin Magnitude WMC-D IOM"
    },
    @{
        Name = "Daikin_IOM1372_Magnitude_WME-D.pdf"
        Url  = "https://tahoeweb.daikinapplied.com/api/general/DownloadDocumentByName/media/IOM1372.pdf/"
        Note = "Daikin Magnitude WME-D IOM"
    }
)

foreach ($f in $files) {
    $out = Join-Path $dest $f.Name
    Write-Host "GET $($f.Url)"
    try {
        Invoke-WebRequest -Uri $f.Url -OutFile $out -UseBasicParsing -Headers @{
            "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        $len = (Get-Item $out).Length
        Write-Host ("  -> {0} ({1:N0} bytes)  {2}" -f $out, $len, $f.Note)
        if ($len -lt 20000) {
            Write-Warning "  File looks too small; may be an HTML bounce page."
        }
    }
    catch {
        Write-Warning "Failed $($f.Name): $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "ASHRAE RP-1043 official report is sold (not a free PDF):"
Write-Host "  https://store.accuristech.com/ashrae/standards/rp-1043-fault-detection-anddiagnostic-fdd-requirements-and-evaluation-toolsfor-chillers?product_id=1716217"
