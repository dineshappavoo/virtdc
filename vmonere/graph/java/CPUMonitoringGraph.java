
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;

import javax.swing.JPanel;
import javax.swing.Timer;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYAreaRenderer;
import org.jfree.data.time.DynamicTimeSeriesCollection;
import org.jfree.data.time.Second;
import org.jfree.data.xy.XYDataset;

/**
 * Class to monitor and produce graph output for CPU usage from logs
 * @author Rahul
 *
 */
public class CPUMonitoringGraph extends JPanel {

	private static final long serialVersionUID = 1L;
	private static final int COUNT = 20;
	private static final int FAST = 500;
	public  BufferedReader br;
	public static String vmid;
	private Timer timer; 
	public CPUMonitoringGraph(String applicationTitle, String chartTitle, String args, BufferedReader bReader, int chartWidth, int chartHeight) {
		super(new BorderLayout());
		br= bReader;
		vmid = args;
		final DynamicTimeSeriesCollection dataset = createDataset();
		JFreeChart chart = createChart(dataset, chartTitle);
		ChartPanel chartPanel = new ChartPanel(chart);
		chartPanel.setPreferredSize(new java.awt.Dimension(chartWidth, chartHeight));
		chartPanel.repaint();
		add(chartPanel, BorderLayout.CENTER);
		timer = new Timer(FAST, new ActionListener() {
			float[] newData = new float[1];
			@Override
			public void actionPerformed(ActionEvent e) {
				newData[0] = fetchCPUData();
				dataset.advanceTime();
				dataset.appendData(newData);
			}
		});
		timer.setInitialDelay(5000);
		timer.setDelay(5000);
	}


	/**
	 * Creates a DynamicTimeSeries dataset for a continuous moving graph 
	 */

	private  DynamicTimeSeriesCollection createDataset() {
		final DynamicTimeSeriesCollection dataset =
				new DynamicTimeSeriesCollection(1, COUNT, new Second());
		dataset.setTimeBase(new Second());
		dataset.addSeries(cpuData(), 0, "CPU data");
		return dataset;
	}


	/**
	 * Creates the continuously updating graph
	 */

	private JFreeChart createChart(final XYDataset dataset, String title) {

		final JFreeChart result = ChartFactory.createTimeSeriesChart(
				title, "", "Value", dataset, true, true, false);
		final XYPlot plot = result.getXYPlot();
		plot.setDomainGridlinesVisible(false);
		plot.setRenderer(new XYAreaRenderer());
		plot.getRenderer().setSeriesPaint(0, Color.BLUE);
		ValueAxis domain = plot.getDomainAxis();
		domain.setAutoRange(true);
		domain.setVisible(false);
		ValueAxis range = plot.getRangeAxis();
		range.setRange(0, 8);
		return result;
	}
	
	/**
	 * Fetches the CPU data from the log file
	 * @return
	 */
	private float fetchCPUData() {
		String currentLine;
		try {
			if ((currentLine = br.readLine()) != null && !currentLine.trim().equals("")) {
				String[] currentValues = currentLine.split("\\|");
				float cpuValue = Float.valueOf(currentValues[2].trim());
				if(cpuValue<0)
				{
					cpuValue = 0;
				}
				else if (cpuValue>800)
				{
					cpuValue = 800;
				}
				return cpuValue;
			}
		} catch (NumberFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return (float) 0.0;
	}

	/**
	 * Set initial values to zero for the first image of the graph
	 * @return
	 */
	private float[] cpuData() {
		float[] a = new float[COUNT];
		for (int i = 0; i < a.length; i++) {
			a[i] = 0;
		}
		return a;
	}

	/**
	 * Start Timer
	 */
	public void start() {
		timer.start();
	}

}  