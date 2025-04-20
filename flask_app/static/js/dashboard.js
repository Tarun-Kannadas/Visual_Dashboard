// Function to create a bar chart using D3.js
function createBarChart(data) {
  const svgWidth = 1200;
  const svgHeight = 600;
  const margin = { top: 20, right: 100, bottom: 200, left: 100 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  // Create SVG container
  const svg = d3.select('#visualization')
                .append('svg')
                .attr('width', svgWidth)
                .attr('height', svgHeight)
                .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`)
                .attr('width', width)
                .attr('height', height);

  // Define scales
  const xScale = d3.scaleBand()
                   .domain(data.map(d => d.title))
                   .range([0, width])
                   .padding(0.1);

  const yScale = d3.scaleLinear()
                   .domain([0, d3.max(data, d => d.intensity)])
                   .nice()
                   .range([height, 0]);

  // Create and append x-axis
  svg.append('g')
     .attr('class', 'x axis')
     .attr('transform', `translate(0,${height})`)
     .call(d3.axisBottom(xScale))
     .selectAll('text')
     .attr('transform', 'rotate(-45)')
     .style('text-anchor', 'end');

  // Create and append y-axis
  svg.append('g')
     .attr('class', 'y axis')
     .call(d3.axisLeft(yScale));

  // Create bars
  svg.selectAll('.bar')
     .data(data)
     .enter()
     .append('rect')
     .attr('class', 'bar')
     .attr('x', d => xScale(d.title))
     .attr('y', d => yScale(d.intensity))
     .attr('width', xScale.bandwidth())
     .attr('height', d => height - yScale(d.intensity))
     .attr('fill', 'steelblue');
}

// Function to update the bar chart based on filtered data
function updateChart(filteredData) {
  const svg = d3.select('#visualization').select('svg').select('g');
  const height = +svg.attr('height');
  const width = +svg.attr('width');
  const xScale = d3.scaleBand()
                   .domain(filteredData.map(d => d.title))
                   .range([0, width])
                   .padding(0.1);
  const yScale = d3.scaleLinear()
                   .domain([0, d3.max(filteredData, d => d.intensity)])
                   .nice()
                   .range([height, 0]);

  svg.select('.x.axis')
     .transition()
     .duration(500)
     .call(d3.axisBottom(xScale))
     .selectAll('text')
     .attr('transform', 'rotate(-45)')
     .style('text-anchor', 'end');

  svg.select('.y.axis')
     .transition()
     .duration(500)
     .call(d3.axisLeft(yScale));

  const bars = svg.selectAll('.bar').data(filteredData, d => d.title);

  bars.exit().remove();

  bars.enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => xScale(d.title))
      .attr('y', d => yScale(d.intensity))
      .attr('width', xScale.bandwidth())
      .attr('height', d => height - yScale(d.intensity))
      .attr('fill', 'steelblue')
      .merge(bars)
      .transition()
      .duration(500)
      .attr('x', d => xScale(d.title))
      .attr('y', d => yScale(d.intensity))
      .attr('width', xScale.bandwidth())
      .attr('height', d => height - yScale(d.intensity));
}

// Function to fetch and update the chart data
function fetchDataAndUpdateChart() {
  const endYear = document.getElementById('end_year').value;
  const topic = document.getElementById('topic').value;
  const sector = document.getElementById('sector').value;
  const region = document.getElementById('region').value;
  const pestle = document.getElementById('pestle').value;
  const source = document.getElementById('source').value;

  const params = new URLSearchParams({
    end_year: endYear,
    topic: topic,
    sector: sector,
    region: region,
    pestle: pestle,
    source: source
  });

  console.log('Fetching data with params:', params.toString()); // Debugging line

  fetch('/data?' + params.toString())
    .then(response => response.json())
    .then(filteredData => {
      console.log('Filtered data received:', filteredData); // Debugging line
      if (filteredData.length === 0) {
        console.log('No data available for the selected filters.');
      }
      updateChart(filteredData);
    })
    .catch(error => console.error('Error fetching or parsing data:', error));
}

// Initial creation of the chart
fetch('/data')
  .then(response => response.json())
  .then(data => {
    createBarChart(data);

    // Add event listeners for filters
    document.querySelectorAll('.filter').forEach(filter => {
      filter.addEventListener('change', fetchDataAndUpdateChart);
    });
  })
  .catch(error => console.error('Error fetching or parsing data:', error));
