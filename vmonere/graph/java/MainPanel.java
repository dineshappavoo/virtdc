/**
 * 
 */

/**
 * @author Rahul
 *
 */
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import com.db.libraryapp.UtilityClasses.ValidationMessage;

/**
 * Main Panel for displaying the input field for VMID and the monitoring graphs
 * @author Rahul
 */
public class MainPanel extends JPanel {
	private static final String PATH = "/var/lib/virtdc/vmonere/monitor_logs/";
	private static final long serialVersionUID = 1L;
	private static String vmid;
	private static MemoryMonitoringGraph memoryChart;
	private static CPUMonitoringGraph cpuChart;
	private static IOMonitoringGraph ioChart;
	public JTextField vmIdTextField;
	public JButton submit;
	public JPanel panel;

	public MainPanel() {
		super(new BorderLayout());
		setPreferredSize(new java.awt.Dimension(1024, 700));
		JPanel labelPanel = new JPanel();
		labelPanel.setSize(200, 100);
		vmIdTextField = new JTextField(20);
		vmIdTextField.setSize(100, 20);
		vmIdTextField.setHorizontalAlignment(SwingConstants.CENTER);
		submit = new JButton("Submit");
		submit.setSize(100,20);
		submit.setHorizontalAlignment(SwingConstants.CENTER);
		//vmIdTextField.setBounds(210, 50, 60, 20);
		JLabel text = new JLabel("VM ID : ");
		text.setHorizontalAlignment(SwingConstants.CENTER);
		text.setForeground(Color.blue);
		text.setFont(new Font("Cambria", Font.BOLD, 20));
		labelPanel.add(text);
		labelPanel.add(vmIdTextField);
		labelPanel.add(submit);
		panel = new JPanel();
		JPanel northPanel = new JPanel();
		try {
			getMemGraph(null);
			getCPUGraph(null);
			getIOGraph(null);
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		if(memoryChart!= null) 
		{
			northPanel.add(memoryChart, BorderLayout.EAST);
		}
		if(cpuChart != null) 
		{
			northPanel.add(cpuChart, BorderLayout.WEST);
		}
		northPanel.setVisible(true);
		panel.add(northPanel, BorderLayout.NORTH);
		if(ioChart != null) 
		{
			panel.add(ioChart, BorderLayout.SOUTH);
		}
		panel.setPreferredSize(new java.awt.Dimension(1024, 600));
		panel.setVisible(false);

		submit.addActionListener(new ActionListener() {
			/**
			 * Action for resetting the graphs for the new VM ID provided in the textfield
			 */
			@Override
			public void actionPerformed(ActionEvent e) {
				if ("".equals(vmIdTextField.getText()) ) {
					ValidationMessage.alertMessage("Please enter the VM Id");
					vmIdTextField.requestFocusInWindow();
				} else {
					try {

						vmid = vmIdTextField.getText();
						((Container) getComponent(1)).removeAll();
						((Container) getComponent(1)).repaint();
						JPanel northPanel = new JPanel();
						getMemGraph(vmid);
						getCPUGraph(vmid);
						getIOGraph(vmid);
						northPanel.add(memoryChart, BorderLayout.EAST);
						northPanel.add(cpuChart, BorderLayout.WEST);
						northPanel.setVisible(true);
						((Container) getComponent(1)).add(northPanel, BorderLayout.NORTH);
						((Container) getComponent(1)).add(ioChart, BorderLayout.SOUTH);
						((Container) getComponent(1)).setPreferredSize(new java.awt.Dimension(1024, 600));
						((Container) getComponent(1)).setVisible(true);
						((Container) getComponent(1)).validate();
					} catch (FileNotFoundException fe) {
						System.out.println(fe.getMessage());
						panel.setVisible(false);
						ValidationMessage.alertMessage("Log for VM-"+vmid+" does not exist!");
					} 
					catch (Exception ex) {
						System.out.println(ex.getMessage());
						ValidationMessage.alertMessage(ex.getMessage());
					}
				}
			}
		});
		add(labelPanel,BorderLayout.NORTH);
		add(panel,BorderLayout.SOUTH);
	}

	/**
	 * Execute monitoring graph for Memory
	 * @param args
	 * @throws IOException 
	 * @throws ParseException 
	 */
	public static void getMemGraph(String args) throws IOException, ParseException  {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			//HH converts hour in 24 hours format (0-23), day calculation
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);

			//in milliseconds
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10000) break;

		}
		memoryChart = new MemoryMonitoringGraph("VM Monitoring", "Memory"+"-"+vmid, vmid, br);
		memoryChart.setVisible(true);
		memoryChart.start();

	}

	/**
	 * Execute monitoring graph for CPU
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getCPUGraph(String args) throws IOException, ParseException {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10000) break;

		}
		cpuChart = new CPUMonitoringGraph("VM Monitoring", "CPU"+"-"+vmid, vmid, br);
		cpuChart.setVisible(true);
		cpuChart.start();

	}

	/**
	 * Execute monitoring graph for IO
	 * @param args
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public static void getIOGraph(String args) throws IOException, ParseException {
		if(args==null) return;
		vmid = args;
		FileInputStream in;
		in = new FileInputStream(PATH+vmid+".log");
		final BufferedReader br = new BufferedReader(new InputStreamReader(in));
		Date currentDate = new Date();
		String currentLine;
		Date d1 = null;
		Date d2 = null;
		while((currentLine = br.readLine()) != null) {
			if(currentLine.trim().equals("")) continue;
			String[] currentValues = currentLine.split("\\|");
			String strCurrLineDate = currentValues[0].trim();
			//HH converts hour in 24 hours format (0-23), day calculation
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSSSSS");
			String strCurrentDate = format.format(currentDate);
			d1 = format.parse(strCurrentDate);
			d2 = format.parse(strCurrLineDate);

			//in milliseconds
			long diff = Math.abs(d2.getTime() - d1.getTime());

			long diffSeconds = diff / 1000;
			if (diffSeconds < 10000) break;

		}
		ioChart = new IOMonitoringGraph("VM Monitoring", "IO"+"-"+vmid, vmid, br);
		ioChart.setVisible(true);
		ioChart.start();
	}

	/**
	 * Initialize Main panel for monitoring
	 */
	private static void startMonitoring() {
		JFrame frame = new JFrame("VM Monitoring Application");
		frame.add(new MainPanel(), BorderLayout.CENTER);
		frame.pack();
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	/**
	 * Main function
	 * @param args
	 */
	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				startMonitoring();
			}
		});
	}
}