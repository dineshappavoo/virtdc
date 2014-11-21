

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.swing.Timer;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.DynamicTimeSeriesCollection;
import org.jfree.data.time.Second;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

import com.monitoring.io.IOMonitoringGraph;

public class MemoryMonitoringGraph extends ApplicationFrame {

	private static final String TITLE = "Memory Monitoring Graph";
	private static final int COUNT = 180;
	private static final int FAST = 100;
	private Timer timer;
	public static BufferedReader br;

	public MemoryMonitoringGraph(final String title) {
		super(title);
		final DynamicTimeSeriesCollection dataset =
				new DynamicTimeSeriesCollection(1, COUNT, new Second());
		dataset.setTimeBase(new Second());
		dataset.addSeries(memData(), 0, "Memory data");
		JFreeChart chart = createMemChart(dataset);


		this.add(new ChartPanel(chart), BorderLayout.CENTER);
		timer = new Timer(FAST, new ActionListener() {
			float[] newData = new float[1];

			@Override
			public void actionPerformed(ActionEvent e) {
				newData[0] = fetchMemData();
				dataset.advanceTime();
				dataset.appendData(newData);
			}
		});
	}

	private float fetchMemData() {
		String currentLine;
		try {
			if ((currentLine = br.readLine()) != null && !currentLine.trim().equals("")) {
				String[] currentValues = currentLine.split("\\|");
				float cpuValue = Float.valueOf(currentValues[2].trim());
				return cpuValue;
			}
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return (float) 0.0;
	}

	private float[] memData() {
		float[] a = new float[COUNT];
		for (int i = 0; i < a.length; i++) {
			a[i] = fetchMemData();
		}
		return a;
	}

	private JFreeChart createMemChart(final XYDataset dataset) {
		final JFreeChart result = ChartFactory.createTimeSeriesChart(
				TITLE, "", "Value", dataset, true, true, false);
		final XYPlot plot = result.getXYPlot();
		ValueAxis domain = plot.getDomainAxis();
		domain.setAutoRange(true);
		ValueAxis range = plot.getRangeAxis();
		range.setRange(0, 50000);
		return result;
	}

	public void start() {
		timer.start();
	}

	public static void main(final String[] args) throws FileNotFoundException {

		if(args.length !=1)
		{
			System.out.println("Please provide valid inputs!");
			return;
		}
		String vmid= args[0];
		FileInputStream in = new FileInputStream("/var/lib/virtdc/logs/monitor_logs/"+vmid+".log");
		br = new BufferedReader(new InputStreamReader(in));
		EventQueue.invokeLater(new Runnable() {

			@Override
			public void run() {
				MemoryMonitoringGraph demo = new MemoryMonitoringGraph(TITLE);
				demo.pack();
				RefineryUtilities.centerFrameOnScreen(demo);
				demo.setVisible(true);
				demo.start();
			}
		});
	}
}
