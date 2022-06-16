import {Component, ElementRef, NgModule, OnInit, ViewChild} from '@angular/core';
import {API_URL, CONFIGURATION, PERFORMANCE, RESOURCE} from '../globals/global_variables';
import {DatePipe} from '@angular/common';
import {CrudService} from '../services/crud.service';

import { HttpClientModule} from '@angular/common/http';
import {AngularEditorConfig, AngularEditorModule} from '@kolkov/angular-editor';



import { jsPDF } from "jspdf";
import html2canvas from 'html2canvas';
import * as math from "mathjs";
@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss'],
  providers: [DatePipe]
})
@NgModule({
  imports: [ HttpClientModule, AngularEditorModule ]
})
export class ReportComponent implements OnInit {


  public date = new Date();
  public allRequestsSum = [0, 0, 0, 0, 0];
  public latencySum = [0, 0, 0,0, 0];
  public errorRateSum = [0, 0, 0,0, 0];
  public sensorsSum = [0, 0, 0,0,0];
  public succRequestsSum = [0, 0, 0, 0, 0];
  public cpuSum = [0, 0, 0, 0, 0];
  public memSum = [0, 0, 0, 0, 0];
  public netOSum = [0, 0, 0, 0, 0];
  public netISum = [0, 0, 0, 0, 0];


  private cpus = [];
  private mems = [];
  private netI = [];
  private netO = [];
  private cpusPerContainer = [];
  private memPerContainer = [];
  private netIperContainer = [];
  private netOperContainer = [];
  private labels = [];
  private labelsPerformance = [];
  private allRequests = [];
  private avgLatency = [];
  private errorRate = [];
  private sensors = [];
  private succRequests = [];
  public metrics: any;
  public performanceMetrics: any;
  private firstLoad: boolean = true;
  public backgroundColor = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
  ];
  public borderColor = [
    'rgba(255,99,132,1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
  ]
  public cpuPerNodeData = [{
    label: "CPU %",
    data: [],
    borderWidth: 1,
    borderColor: this.borderColor[0],
    backgroundColor: this.backgroundColor[0],
    fill: false
  }];
  public memPerNodeData = [];
  public netInPerNodeData = [];
  public netOuPerNodeData = [];

  cpuData = [{
    label: 'Average CPU %',
    data: this.cpus,
    borderWidth: 1,
    fill: false
  }];
  memData = [{
    label: 'Average MEM %',
    data: this.mems,
    borderWidth: 1,
    fill: false
  }];

  netInData = [{
    label: 'Average Net Input (B)',
    data: this.netI,
    borderWidth: 1,
    fill: false
  }];
  netOuData = [{
    label: 'Average Net output (B)',
    data: this.netO,
    borderWidth: 1,
    fill: false
  }];

  requestsData = [{
    label: '# Emit rate',
    data: this.allRequests,
    borderWidth: 1,
    fill: false,
    borderColor: this.borderColor[0],
    backgroundColor: this.backgroundColor[0],
  }, {
    label: '# Throughput',
    data: this.succRequests,
    borderWidth: 1,
    fill: false,
    borderColor: this.borderColor[1],
    backgroundColor: this.backgroundColor[1],
  }
  ];
  latencyData = [{
    label: 'Average latency (ms)',
    data: this.avgLatency,
    borderWidth: 1,
    fill: false
  }];

  errorRateData = [{
    label: 'Error Rate',
    data: this.errorRate,
    borderWidth: 1,
    fill: false
  }];
  sensorsData = [{
    label: '# Number of users',
    data: this.sensors,
    borderWidth: 1,
    fill: false
  }];


  lineChartLabels = this.labels;
  lineChartLabelsPerformance = this.labelsPerformance;

  lineChartOptions = {

    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Time',
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true
        },
        ticks: {
          beginAtZero: true,
          suggestedMax: 100,
        }
      }]
    },
    legend: {
      display: true
    },
    elements: {
      point: {
        radius: 0
      }
    }
  };

  lineChartOptionsPerformance = {

    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Time',
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true
        },
        ticks: {
          beginAtZero: true
        }
      }]
    },
    legend: {
      display: true
    },
    elements: {
      point: {
        radius: 0
      }
    }
  };

  lineChartColors = [
    {
      borderColor: 'rgba(255,99,132,1)'
    }
  ];

  config: AngularEditorConfig = { editable: true, spellcheck: true, height: '15rem', minHeight: '5rem', placeholder: 'Enter text here...', translate: 'no' }

  public receivers = ""
  public receiversTable = []
  public blockchain = ""
  public consensus = ""
  public nodes = 0
  public size = 1
  htmlContent: any;


  constructor(private crudService: CrudService,
              private datePipe: DatePipe) {
  }

  ngOnInit(): void {
    this.getResourceMetrics()
    this.getPerformanceMetrics()
    this.getConfiguration()
  }

  getConfiguration() {
    this.crudService.getAll(API_URL + CONFIGURATION).subscribe(
      (response) => {
        console.log(response.data)
        this.blockchain = response.data.blockchain
        this.consensus = response.data.consensus
        this.nodes = response.data.nodes
        this.size = response.data.size
        this.receiversTable = response.data.receivers
        // this.receivers =response.data.receivers.join('\r\n')
        this.receivers =response.data.receivers.join(' ,   ')


      });
  }

  getResourceMetrics() {
    this.crudService.getAll(API_URL + RESOURCE).subscribe(
      (response) => {
        console.log(response)
        this.metrics = response.data
        this.metrics.forEach(
          x => {
            this.splitData(x)
          })
        this.setCpuPerNodeData()
        this.setMemPerNodeData()
        this.setNetInPerNodeData()
        this.setNetOuPerNodeData()
        this.firstLoad = false
      });

  }

  getPerformanceMetrics() {
    this.crudService.getAll(API_URL + PERFORMANCE).subscribe(
      (response) => {
        console.log(response)
        this.performanceMetrics = response.data
        this.performanceMetrics.forEach(
          x => {
            this.splitDataPerformance(x)
          })

      });
  }

  splitData(data) {
    this.labels.push(this.datePipe.transform(data.time, 'hh:mm:ss'))
    this.cpus.push(data.avgCPU)
    this.mems.push(data.avgMEM)
    this.netI.push(data.avgNetI)
    this.netO.push(data.avgNetO)
    if (data.containers) {
      data.containers.forEach(
        x => {
          if (!this.cpusPerContainer[x.name]) {
            this.cpusPerContainer[x.name] = []
            this.memPerContainer[x.name] = []
            this.netIperContainer[x.name] = []
            this.netOperContainer[x.name] = []
          }
          this.cpusPerContainer[x.name].push(x.cpu)
          this.memPerContainer[x.name].push(x.mem)
          this.netIperContainer[x.name].push(x.netI)
          this.netOperContainer[x.name].push(x.netO)
        }
      )
    }
    this.calculateSummaryResource()
  }

  calculateSummaryPerformance() {
    this.allRequestsSum[0] = math.mean(this.allRequests)
    this.allRequestsSum[1] = math.variance(this.allRequests)
    this.allRequestsSum[2] = math.std(this.allRequests)
    this.allRequestsSum[3] = math.min(this.allRequests)
    this.allRequestsSum[4] = math.max(this.allRequests)

    this.latencySum[0] = math.mean(this.avgLatency)
    this.latencySum[1] = math.variance(this.avgLatency)
    this.latencySum[2] = math.std(this.latencySum)
    this.latencySum[3] = math.min(this.latencySum)
    this.latencySum[4] = math.max(this.latencySum)

    this.errorRateSum[0] = math.mean(this.errorRate)
    this.errorRateSum[1] = math.variance(this.errorRate)
    this.errorRateSum[2] = math.std(this.errorRate)
    this.errorRateSum[3] = math.min(this.errorRate)
    this.errorRateSum[4] = math.max(this.errorRate)

    this.succRequestsSum[0] = math.mean(this.succRequests)
    this.succRequestsSum[1] = math.variance(this.succRequests)
    this.succRequestsSum[2] = math.std(this.succRequests)
    this.succRequestsSum[3] = math.min(this.succRequests)
    this.succRequestsSum[4] = math.max(this.succRequests)

    this.sensorsSum[0] = math.mean(this.sensors)
    this.sensorsSum[1] = math.variance(this.sensors)
    this.sensorsSum[2] = math.std(this.sensors)
    this.sensorsSum[3] = math.min(this.sensors)
    this.sensorsSum[4] = math.max(this.sensors)

  }

  splitDataPerformance(data) {

    this.labelsPerformance.push(this.datePipe.transform(data.time, 'hh:mm:ss'))
    this.allRequests.push(data.allRequests)
    this.avgLatency.push(data.avgLatency)
    this.errorRate.push(data.errorRate)
    this.succRequests.push(data.succRequests)
    this.sensors.push(data.sensors)
    this.calculateSummaryPerformance()

  }

  setCpuPerNodeData() {

    var i = 0;
    if (this.firstLoad) {
      this.cpuPerNodeData.pop()
    }

    for (let name in this.cpusPerContainer) {

      this.cpuPerNodeData.push({
        data: this.cpusPerContainer[name],
        label: name,
        borderWidth: 1,
        borderColor: this.borderColor[i],
        backgroundColor: this.backgroundColor[i],
        fill: false
      })
      i++;
    }
      this.cpuPerNodeData.push({
       data: this.cpus,
        label: 'Average ',
        borderWidth: 1,
        borderColor: 'black',
        backgroundColor: 'black',
        fill: false
      })

  }

  setMemPerNodeData() {
    var i = 0;
    if (this.firstLoad) {
      this.memPerNodeData.pop()
    }
    for (let name in this.memPerContainer) {

      this.memPerNodeData.push({
        data: this.memPerContainer[name],
        label: name,
        borderWidth: 1,
        borderColor: this.borderColor[i],
        backgroundColor: this.backgroundColor[i],
        fill: false
      })
      i++;
    }
   this.memPerNodeData.push({
          data: this.mems,
          label: 'Average',
          borderWidth: 1,
          borderColor: 'black',
          backgroundColor: 'black',
          fill: false
        })
  }

  setNetInPerNodeData() {
    var i = 0;
    if (this.firstLoad) {
      this.netInPerNodeData.pop()
    }
    for (let name in this.netIperContainer) {

      this.netInPerNodeData.push({
        data: this.netIperContainer[name],
        label: name,
        borderWidth: 1,
        borderColor: this.borderColor[i],
        backgroundColor: this.backgroundColor[i],
        fill: false
      })
      i++;
    }
    this.netInPerNodeData.push({
             label: 'Average',
             data: this.netI,
            borderWidth: 1,
            borderColor: 'black',
            backgroundColor: 'black',
            fill: false
          })

  }

   setNetOuPerNodeData() {
    var i = 0;
    if (this.firstLoad) {
      this.netOuPerNodeData.pop()
    }
    for (let name in this.netOperContainer) {

      this.netOuPerNodeData.push({
        data: this.netOperContainer[name],
        label: name,
        borderWidth: 1,
        borderColor: this.borderColor[i],
        backgroundColor: this.backgroundColor[i],
        fill: false
      })
      i++;
    }
    this.netOuPerNodeData.push({
           label: 'Average',
           data: this.netO,
          borderWidth: 1,
          borderColor: 'black',
          backgroundColor: 'black',
          fill: false
        })
  }



  calculateSummaryResource() {
    this.cpuSum[0] = math.mean(this.cpus)
    this.cpuSum[1] = math.variance(this.cpus)
    this.cpuSum[2] = math.std(this.cpus)
    this.cpuSum[3] = math.min(this.cpus)
    this.cpuSum[4] = math.max(this.cpus)

    this.memSum[0] = math.mean(this.mems)
    this.memSum[1] = math.variance(this.mems)
    this.memSum[2] = math.std(this.mems)
    this.memSum[3] = math.min(this.mems)
    this.memSum[4] = math.max(this.mems)

    this.netISum[0] = math.mean(this.netI)
    this.netISum[1] = math.variance(this.netI)
    this.netISum[2] = math.std(this.netI)
    this.netISum[3] = math.min(this.netI)
    this.netISum[4] = math.max(this.netI)

    this.netOSum[0] = math.mean(this.netO)
    this.netOSum[1] = math.variance(this.netO)
    this.netOSum[2] = math.std(this.netO)
    this.netOSum[3] = math.min(this.netO)
    this.netOSum[4] = math.max(this.netO)

  }


  public downloadAsPDF2() {
    var data = document.getElementById('print');
    let pdf = new jsPDF('p', 'mm', 'a4');
    html2canvas(data).then(canvas => {
      var imgWidth = 208;
      var imgHeight = canvas.height * imgWidth / canvas.width;
      const contentDataURL = canvas.toDataURL('image/png')

      var position = 0;
      pdf.addImage(contentDataURL, 'PNG', 0, position, imgWidth, imgHeight)

    });


  }

  public downloadAsPDF(){
    var data = document.getElementById('print');
    html2canvas(data).then(canvas => {
      var imgData = canvas.toDataURL('image/png');

      /*
      Here are the numbers (paper width and height) that I found to work.
      It still creates a little overlap part between the pages, but good enough for me.
      if you can find an official number from jsPDF, use them.
      */
      var imgWidth = 210;
      var pageHeight = 295;
      var imgHeight = canvas.height * imgWidth / canvas.width;
      var heightLeft = imgHeight;

      var doc = new jsPDF('p', 'mm');
      var position = 0;

      doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        doc.addPage();
        doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }
      doc.save("blockCompass-report" + '.pdf');

    });
  }

}
